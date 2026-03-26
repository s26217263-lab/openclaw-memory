#!/bin/bash
set -euo pipefail

export PATH="/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:$PATH"

WORKSPACE="/Users/palpet/.openclaw/workspace"
BACKUP_ROOT="$WORKSPACE/backups/openclaw"
DATE_STAMP="$(date '+%Y-%m-%d')"
TIME_STAMP="$(date '+%H%M%S')"
TARGET_DIR="$BACKUP_ROOT/$DATE_STAMP/$TIME_STAMP"
LATEST_LINK="$BACKUP_ROOT/latest"
LOG_DIR="$WORKSPACE/logs"
LOG_FILE="$LOG_DIR/nightly_openclaw_backup.log"

mkdir -p "$TARGET_DIR" "$LOG_DIR"

log() {
  printf '[%s] %s\n' "$(date '+%Y-%m-%d %H:%M:%S')" "$*" | tee -a "$LOG_FILE"
}

copy_if_exists() {
  local src="$1"
  local dst="$2"
  if [ -e "$src" ]; then
    mkdir -p "$(dirname "$dst")"
    cp -R "$src" "$dst"
    log "copied: $src"
  else
    log "missing, skipped: $src"
  fi
}

log "backup start -> $TARGET_DIR"

# Core identity/memory files
copy_if_exists "$WORKSPACE/SOUL.md" "$TARGET_DIR/workspace/SOUL.md"
copy_if_exists "$WORKSPACE/USER.md" "$TARGET_DIR/workspace/USER.md"
copy_if_exists "$WORKSPACE/IDENTITY.md" "$TARGET_DIR/workspace/IDENTITY.md"
copy_if_exists "$WORKSPACE/TOOLS.md" "$TARGET_DIR/workspace/TOOLS.md"
copy_if_exists "$WORKSPACE/AGENTS.md" "$TARGET_DIR/workspace/AGENTS.md"
copy_if_exists "$WORKSPACE/MEMORY.md" "$TARGET_DIR/workspace/MEMORY.md"

# Memory files
copy_if_exists "$WORKSPACE/memory" "$TARGET_DIR/workspace/memory"

# OpenClaw config
copy_if_exists "/Users/palpet/.openclaw/openclaw.json" "$TARGET_DIR/openclaw/openclaw.json"
copy_if_exists "/Users/palpet/.openclaw/cron/jobs.json" "$TARGET_DIR/openclaw/cron-jobs.json"

# Agent configs (main, ops, ecompass)
copy_if_exists "/Users/palpet/.openclaw/agents/main" "$TARGET_DIR/agents/main"
copy_if_exists "/Users/palpet/.openclaw/agents/ops" "$TARGET_DIR/agents/ops"
copy_if_exists "/Users/palpet/.openclaw/agents/ecompass" "$TARGET_DIR/agents/ecompass"

# Projects (ecompass)
copy_if_exists "$WORKSPACE/projects" "$TARGET_DIR/workspace/projects"

# Skills (selective - only persistent custom ones)
copy_if_exists "$WORKSPACE/skills/jimeng-auto-generator" "$TARGET_DIR/skills/jimeng-auto-generator"
copy_if_exists "$WORKSPACE/skills/video-production-automation" "$TARGET_DIR/skills/video-production-automation"
copy_if_exists "$WORKSPACE/skills/video-script-generator" "$TARGET_DIR/skills/video-script-generator"
copy_if_exists "$WORKSPACE/skills/video-to-jimeng-images" "$TARGET_DIR/skills/video-to-jimeng-images"
copy_if_exists "$WORKSPACE/skills/tavily-search-skill" "$TARGET_DIR/skills/tavily-search-skill"

# Scripts
copy_if_exists "$WORKSPACE/scripts/nightly_openclaw_backup.sh" "$TARGET_DIR/scripts/nightly_openclaw_backup.sh"
copy_if_exists "$WORKSPACE/scripts/watchdog_openclaw.sh" "$TARGET_DIR/scripts/watchdog_openclaw.sh"

log "local backup complete"

# Prune old local backups
find "$BACKUP_ROOT" -mindepth 1 -maxdepth 1 -type d -mtime +7 -exec rm -rf {} +
log "pruned local backups older than 7 days"

# Push to GitHub via API (skips git to avoid credential hanging issues)
if [ -n "${GH_TOKEN:-${GITHUB_TOKEN:-}}" ]; then
  log "pushing backup to GitHub..."
  python3 - "$TARGET_DIR" << 'PYEOF'
import os, sys, base64, json, urllib.request, urllib.error

backup_dir = sys.argv[1]
repo = "s26217263-lab/openclaw-memory"
branch = "main"
token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN", "")

def gh(method, path, data=None):
    url = f"https://api.github.com{path}"
    h = {"Authorization": f"token {token}", "Accept": "application/vnd.github.v3+json"}
    body = None
    if data:
        body = json.dumps(data).encode()
        h["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=body, headers=h, method=method)
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"  GH API error: {e}")
        return None

ref = gh("GET", f"/repos/{repo}/git/refs/heads/{branch}")
if not ref:
    print("  failed to get ref"); sys.exit(1)
sha = ref["object"]["sha"]

# Collect files (essential only, skip large dirs)
skip = {".git", "workspace", "skills", "_disabled", "node_modules", "__pycache__"}
files = []
for root, dirs, filenames in os.walk(backup_dir):
    dirs[:] = [d for d in dirs if d not in skip]
    for fname in filenames:
        fpath = os.path.join(root, fname)
        rel = os.path.relpath(fpath, backup_dir)
        try:
            with open(fpath, "rb") as f:
                content = base64.b64encode(f.read()).decode()
            files.append({"path": rel, "content": content})
        except Exception as e:
            print(f"  skip {rel}: {e}")

print(f"files: {len(files)}")
if not files:
    print("  nothing to push"); sys.exit(0)

# Create blobs
for f in files:
    blob = gh("POST", f"/repos/{repo}/git/blobs", {"content": f["content"], "encoding": "base64"})
    if blob:
        f["sha"] = blob["sha"]
    else:
        print(f"  blob failed: {f['path']}")

blobs = [{"path": f["path"], "mode": "100644", "type": "blob", "sha": f["sha"]} for f in files if "sha" in f]
print(f"blobs: {len(blobs)}")

tree = gh("POST", f"/repos/{repo}/git/trees", {"base_tree": sha, "tree": blobs})
if not tree:
    print("  tree failed"); sys.exit(1)

commit = gh("POST", f"/repos/{repo}/git/commits", {
    "message": f"Backup {os.path.basename(backup_dir)}",
    "tree": tree["sha"],
    "parents": [sha]
})
if not commit:
    print("  commit failed"); sys.exit(1)

result = gh("PATCH", f"/repos/{repo}/git/refs/heads/{branch}", {"sha": commit["sha"]})
if result:
    print(f"  pushed {len(blobs)} files to GitHub")
else:
    print("  ref update failed")
PYEOF
else
  log "GH_TOKEN not set; skipped GitHub push"
fi

ln -sfn "$TARGET_DIR" "$LATEST_LINK"
log "backup complete"
