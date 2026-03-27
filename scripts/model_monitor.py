#!/usr/bin/env python3
"""
Model Health Monitor — GPT-5.4 vs MiniMax-M2.7 Auto-Switch

Strategy:
- gpt-5.4 is accessed via OAuth (browser session) — cannot be probed directly
- Instead: track when we SWITCHED to fallback (reactive), then retry after cooldown
- Each heartbeat call infers primary status from whether the session is on fallback
- After FALLBACK_COOLDOWN_HOURS on MiniMax → attempt primary again
- The "attempt" is just setting it as active; if it's still down, the next 429 will re-trigger

State file: state/model_state.json
  active_model: current model
  fallback_start: ISO timestamp when we switched to fallback
  last_known_primary_ok: bool (updated when on primary)
  last_switch: ISO timestamp
  switch_reason: string

Cooldown: 2 hours on fallback before retrying primary
"""

import json
import os
import sys
from datetime import datetime, timezone, timedelta
from typing import Optional

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
WORKSPACE = os.path.dirname(SCRIPT_DIR)
STATE_FILE = os.path.join(WORKSPACE, "state", "model_state.json")
os.makedirs(os.path.dirname(STATE_FILE), exist_ok=True)

PRIMARY_MODEL = "openai-codex/gpt-5.4"
FALLBACK_MODEL = "minimax/MiniMax-M2.7"
FALLBACK_COOLDOWN_HOURS = 2

# ── State ───────────────────────────────────────────────────────────────────

def load_state() -> dict:
    if os.path.exists(STATE_FILE):
        try:
            with open(STATE_FILE) as f:
                return json.load(f)
        except Exception:
            pass
    return {
        "active_model": PRIMARY_MODEL,
        "fallback_start": None,
        "last_known_primary_ok": True,
        "last_switch": None,
        "switch_reason": None,
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }

def save_state(state: dict) -> None:
    state["last_updated"] = datetime.now(timezone.utc).isoformat()
    with open(STATE_FILE, "w") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)

# ── External signals (written by external triggers) ──────────────────────────

def record_rate_limit():
    """Call this when a 429 is detected from primary → switch to fallback."""
    state = load_state()
    if state["active_model"] != FALLBACK_MODEL:
        state["active_model"] = FALLBACK_MODEL
        state["fallback_start"] = datetime.now(timezone.utc).isoformat()
        state["last_switch"] = datetime.now(timezone.utc).isoformat()
        state["switch_reason"] = "rate_limit_429"
        save_state(state)
        print(f"[{state['last_updated']}] 429 detected → switched to {FALLBACK_MODEL}")
    else:
        # Already on fallback, just update timestamp
        state["fallback_start"] = datetime.now(timezone.utc).isoformat()
        save_state(state)

def record_primary_ok():
    """Call this when primary responds successfully (after a switch-back)."""
    state = load_state()
    if state["active_model"] != PRIMARY_MODEL:
        state["active_model"] = PRIMARY_MODEL
        state["fallback_start"] = None
        state["last_known_primary_ok"] = True
        state["last_switch"] = datetime.now(timezone.utc).isoformat()
        state["switch_reason"] = "primary_recovered"
        save_state(state)
        print(f"[{state['last_updated']}] Primary OK → switched back to {PRIMARY_MODEL}")
    else:
        state["last_known_primary_ok"] = True
        save_state(state)

def get_active_model() -> str:
    """Returns the currently preferred model."""
    return load_state().get("active_model", PRIMARY_MODEL)

def get_fallback_remaining_hours() -> Optional[float]:
    """Hours remaining before we can retry primary. None if on primary or no fallback_start."""
    state = load_state()
    if state["active_model"] != FALLBACK_MODEL:
        return None
    if not state.get("fallback_start"):
        return 0.0
    try:
        start = datetime.fromisoformat(state["fallback_start"])
        if start.tzinfo is None:
            start = start.replace(tzinfo=timezone.utc)
    except Exception:
        return None
    now = datetime.now(timezone.utc)
    elapsed_hours = (now - start).total_seconds() / 3600
    remaining = FALLBACK_COOLDOWN_HOURS - elapsed_hours
    return max(0.0, remaining)

# ── Heartbeat check (called by heartbeat cron/agent) ───────────────────────

def run_heartbeat_check(current_session_model: Optional[str] = None) -> dict:
    """
    Called by heartbeat every ~30 min.
    current_session_model: pass the model's name if known, else None to infer from state.
    Returns the decision dict.
    """
    state = load_state()
    now = datetime.now(timezone.utc).isoformat()
    decision = {"action": "none", "active_model": state["active_model"], "reason": ""}

    if state["active_model"] == FALLBACK_MODEL:
        # On fallback — check if cooldown has passed
        remaining = get_fallback_remaining_hours()
        if remaining is not None and remaining <= 0:
            # Cooldown done — try primary again
            state["active_model"] = PRIMARY_MODEL
            state["fallback_start"] = None
            state["last_switch"] = now
            state["switch_reason"] = "cooldown_complete_try_primary"
            state["last_known_primary_ok"] = False  # optimistic, will be confirmed on first success
            save_state(state)
            decision = {
                "action": "switch_to_primary",
                "active_model": PRIMARY_MODEL,
                "reason": f"Cooldown complete ({FALLBACK_COOLDOWN_HOURS}h). Primary re-selected. "
                          f"If still rate-limited, next 429 will re-trigger fallback."
            }
        else:
            decision = {
                "action": "stay_on_fallback",
                "active_model": FALLBACK_MODEL,
                "reason": f"On fallback. {remaining:.1f}h until next primary retry."
            }
    else:
        # On primary — record as ok (heartbeat confirms liveness)
        state["last_known_primary_ok"] = True
        save_state(state)
        decision = {
            "action": "ok",
            "active_model": PRIMARY_MODEL,
            "reason": "Primary available. No action needed."
        }

    # Always output for log visibility
    print(f"[{now}] Model monitor heartbeat:")
    print(f"  Action: {decision['action']}")
    print(f"  Active: {decision['active_model']}")
    print(f"  Reason: {decision['reason']}")
    if state.get("fallback_start"):
        remaining = get_fallback_remaining_hours()
        print(f"  Fallback remaining: {remaining:.1f}h" if remaining else "  Fallback: cooling down...")

    return decision

# ── CLI / entry point ───────────────────────────────────────────────────────

if __name__ == "__main__":
    # Allow passing current session model as argument
    current = sys.argv[1] if len(sys.argv) > 1 else None
    result = run_heartbeat_check(current_session_model=current)
    sys.exit(0)
