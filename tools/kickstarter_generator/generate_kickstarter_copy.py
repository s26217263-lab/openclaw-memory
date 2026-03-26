#!/usr/bin/env python3
import json
from pathlib import Path

ROOT = Path('/Users/palpet/.openclaw/workspace/tools/kickstarter_generator')
INPUT = ROOT / 'product_input_template.json'
OUT = ROOT / 'generated_kickstarter_copy.md'

with INPUT.open() as f:
    data = json.load(f)

name = data['product_name']
tagline = data['tagline']
market = data['market']
ptype = data['product_type']
audience = ', '.join(data['target_audience'])
benefits = data['core_benefits']
rewards = data['reward_tiers']

reward_lines = []
for r in rewards:
    reward_lines.append(f"## {r['name']} — ${r['price_usd']}\n" + '\n'.join([f"- {x}" for x in r['includes']]))

md = f"""# {name} Kickstarter Copy Pack v1

## Project Title
{name} — A Cyber-Feng-Shui Ritual Object

## Short Blurb
{tagline}

## Market
{market}

## Product Type
{ptype}

## Target Audience
{audience}

## Core Value Proposition
{name} combines a tactile desk object with a web-based AI ritual. You spin the compass, open your personalized web experience, and get one clear prompt: what matters most today? From there, the AI helps you stay focused, reflect, and finish the day with direction.

## Why It Matters
Most productivity tools live inside your screen. {name} starts on your desk, in your hand, through a deliberate physical action. That small ritual turns scattered attention into focused momentum.

## Core Benefits
""" + '\n'.join([f"- {b}" for b in benefits]) + f"""

## Reward Tiers

""" + '\n\n'.join(reward_lines) + f"""

## FAQ
### What is {name}?
{name} is a physical ritual compass paired with a web-based AI companion.

### How does it work?
You tap or scan the compass and enter a guided web experience that helps you reset, focus, and reflect.

### Is this a meditation product?
Not exactly. It is a daily ritual object designed for calm, direction, and sustained progress.

## Risks & Challenges
- Manufacturing consistency for the compass body
- NFC integration and durability
- Cross-cultural storytelling for Kickstarter audiences

## Timeline
- Prototype validation
- Campaign launch before May 1
- Manufacturing confirmation after funding
- Delivery after production window
"""

OUT.write_text(md)
print(f'Generated: {OUT}')
