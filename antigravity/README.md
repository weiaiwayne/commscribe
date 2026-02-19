# CommScribe for Google Antigravity

This directory contains CommScribe adapted for Google's Antigravity (Gemini) agent framework.

## Installation

```bash
# Clone CommScribe
git clone https://github.com/weiaiwayne/commscribe.git

# Copy Antigravity version to your Gemini skills
cp -r commscribe/antigravity/* ~/.gemini/antigravity/skills/commscribe/
```

## Structure

```
antigravity/
├── SKILL.md              # Main entry point (Gemini format)
├── references/
│   ├── stages/           # 4-stage workflow
│   ├── voice/            # Voice learning
│   ├── anti-ai/          # Pattern avoidance
│   └── workflows/        # Validation, nudges
└── scripts/
    └── zotero_adapt.py   # Zotero integration
```

## Usage

After installation, Gemini will recognize CommScribe triggers:

```
Write a literature review on networked gatekeeping

→ CommScribe activates
→ Asks for concept validation (300+ words, 3+ citations)
→ Proceeds through 4-stage workflow
```

## Differences from OpenClaw Version

| Feature | OpenClaw | Antigravity |
|---------|----------|-------------|
| Multi-agent | `sessions_spawn` | Gemini tool calls |
| Voice profiles | JSON files | Same |
| Zotero | Same API | Same API |
| Anti-AI patterns | Same | Same |

## Zotero Setup

Same as main version:

```bash
export ZOTERO_USER_ID="your_user_id"
export ZOTERO_API_KEY="your_api_key"
```

---

*Part of CommScribe — Literature Review & Theorization Framework*
