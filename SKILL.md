---
name: commscribe
description: Unblock your scholarship — helps with writer's block while keeping your voice central
metadata: {"clawdbot":{"emoji":"✍️"}}
---

# /commscribe - Scholarly Writing Assistant

> **Auto-Update:** This skill auto-pulls from GitHub on load. Run `git pull` in skill directory for manual update.

**Location:** `~/clawd/skills/commscribe/`
**GitHub:** https://github.com/weiaiwayne/commscribe

## First: Auto-Update Check

Before using CommScribe, pull latest:

```bash
cd ~/clawd/skills/commscribe && git pull --ff-only
```

Then read:
- `skill-templates/SKILL.md` for detailed workflow
- `samples/voice_profiles/` for voice profile examples

---

## Quick Reference

### Start Literature Review
```
/commscribe start lit review on [topic]
```

### Setup Voice Profile
```
/commscribe setup voice
```

### Check Draft
```
/commscribe check [paste or describe draft]
```

### Audit Draft
```
/commscribe audit
```

---

## The 4-Stage Workflow

| Stage | Purpose | Gate |
|-------|---------|------|
| **1. Concept** | Validate research question | 300+ words, 3+ citations |
| **2. Synthesis** | Search & integrate literature | Zotero + API search |
| **3. Drafting** | Write in user's voice | Voice profile + anti-AI |
| **4. Audit** | Independent critical review | Different model reviews |

---

## Voice Learning

CommScribe learns YOUR writing style from samples:
- Extract from 5-10 of your papers (500+ words each)
- Matches sentence length, hedging, transitions
- Avoids 286 AI-typical patterns

---

## Key Files

| File | Purpose |
|------|---------|
| `skill-templates/SKILL.md` | Full workflow documentation |
| `skill-templates/stages/` | Stage-specific guides |
| `skill-templates/voice/` | Voice extraction & prompting |
| `skill-templates/anti-ai/` | Pattern avoidance |
| `scripts/` | Python modules |
| `openclaw/AGENTS.md` | Multi-agent workflow |

---

## Integration with CommDAAF

CommScribe handles writing; CommDAAF handles data analysis.

```
Research Project
├── Literature (CommScribe)
│   └── Theory → Synthesis → Writing
└── Data (CommDAAF)
    └── Collection → Analysis → Results
```

---

*Your ideas. Your voice. We just help you get unstuck.*
