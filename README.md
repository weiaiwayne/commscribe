# CommScribe

**Your Research Writing Partner** | v0.2.0

*I write with you. I learn from you. I push back when you need it.*

**Sister project to [CommDAAF](https://github.com/weiaiwayne/commDAAF)** — while CommDAAF handles data analysis, CommScribe handles literature review, theory building, and scholarly writing.

---

## Not a Yes-Man

I'm your research assistant, not your ghostwriter.

**I will:**
- Write *with* you — drafting, revising, thinking alongside
- Learn your voice, your preferences, your quirks
- Push back when your argument is weak
- Tell you when something doesn't make sense
- Catch the mistakes you've made before
- Get better the more we work together

**I won't:**
- Write your paper while you do something else
- Generate arguments for positions you haven't thought through
- Make weak ideas sound impressive
- Let you treat me as a shortcut
- Say "great idea!" when it isn't

---

## ⚠️ Experimental Software

Under active development at [LampBotics AI Lab](https://lampbotics.com). Use with caution.

---

## The Deal

You bring the thinking. I bring the craft.

You know your research. I know writing mechanics, literature search, and how to unstick your brain when you've been staring at the same paragraph for an hour.

When you ask me to do something that crosses into "do my work for me" territory, I'll say no — and explain why. That's not me being difficult. That's me being useful.

### What I Won't Do

| Request | My Response |
|---------|-------------|
| "Write me a literature review" | ❌ No. What's your argument? I'll help you draft *after* you tell me what you think. |
| "Make this sound smarter" | ❌ No. If the idea is weak, better prose won't save it. |
| "Just fix it for me" | ❌ No. Tell me what's wrong, we'll fix it together. |
| "Generate some arguments for..." | ❌ No. Arguments come from thinking, not prompts. |

If you want a tool that writes papers while you sleep, this isn't it.

---

## The Problem: Getting Stuck

Every academic knows the feeling:

- **The blank page** — you know what you want to say, but can't start
- **Literature overwhelm** — drowning in papers, can't see the synthesis
- **The muddy middle** — draft exists, but it's not *clicking*
- **Voice fatigue** — after hours of writing, you don't sound like yourself anymore
- **Revision paralysis** — something's wrong, but you can't see it

These aren't signs you can't write. They're signs you're human.

---

## What CommScribe Does

**Helps you get unstuck — while keeping YOUR voice at the center.**

| When You're Stuck On... | CommScribe Helps By... |
|-------------------------|------------------------|
| Starting | Structured concept validation gets ideas flowing |
| Literature | Searches, organizes, synthesizes — you focus on meaning |
| Drafting | Learns YOUR voice, offers scaffolding in YOUR style |
| Revising | Independent audit spots what you can't see anymore |
| Consistency | Maintains your voice even when you're exhausted |

**The ideas are yours. The arguments are yours. The voice is yours.**

We just handle the friction that gets in the way.

---

## Your Voice at the Center

Most AI writing tools have a voice problem: they make everyone sound the same.

CommScribe flips this:

1. **Learns YOUR writing style** — from your own papers, your own words
2. **Generates in YOUR voice** — not "academic writing," YOUR academic writing
3. **Blocks generic patterns** — 286 AI-typical phrases that would dilute your voice
4. **Adapts with feedback** — tell it "that sounds like me" or "that doesn't," it learns

The result: drafts that sound like you wrote them on a good day — because they're built on YOUR patterns, not generic ones.

---

## Core Features

---

## Heritage

CommScribe shares DNA with:
- **[CommDAAF](https://github.com/weiaiwayne/commDAAF)** — Research integrity, tiered validation, nudge system
- **[DAAF](https://github.com/DAAF-Contribution-Community/daaf)** — Original methodological framework

| CommDAAF | CommScribe |
|----------|------------|
| Data analysis | Literature review |
| Methods validation | Draft validation |
| Network/text analysis | Synthesis/theorization |
| Results interpretation | Argument construction |
| Post-API data strategies | Voice learning |

---

### 🎤 Voice Learning

**Two modes available:**

#### Statistical Mode (Traditional)
- Sentence length patterns
- Vocabulary richness
- Hedging preferences ("suggests" vs "proves")
- Transition usage
- Citation integration style

#### Adaptive Mode (AI-Native) ⭐ NEW
- **Embedding-based** — captures the gestalt, not just word counts
- **Continuous learning** — improves with each "sounds like me" / "doesn't" feedback
- **Contrastive** — learns what your voice is NOT (vs AI, vs generic academic)
- **Calibrating threshold** — adapts to YOUR preferences over time

```python
# Adaptive voice improves with use
manager.feedback("wayne", generated_text, sounds_like_me=True)
```

Generated text matches YOUR voice, not generic academic-ese.

### 🚫 Anti-AI Pattern Awareness

286 patterns to avoid across 10 categories:
- Generic openers ("In recent years...")
- Importance phrases ("It is important to note...")
- Overused transitions ("Furthermore, Moreover, Additionally")
- Excessive hedging ("could potentially possibly")
- Filler phrases ("a wide range of", "plays a crucial role")
- Structural patterns ("Let's dive in", "Here are 5 tips")
- Inflated adjectives ("groundbreaking", "transformative")
- Emoji in academic text (🔑💡✨)
- Academic AI patterns ("This paper aims to fill a gap")
- Conclusion clichés ("In conclusion", "All in all")

### 📚 4-Stage Workflow

| Stage | Purpose | Key Feature |
|-------|---------|-------------|
| **1. Concept** | Define research question | Validation gate (300+ words, 3+ citations) |
| **2. Synthesis** | Literature search & integration | Zotero KG + OpenAlex + semantic search |
| **3. Drafting** | Write in your voice | Voice-constrained generation |
| **4. Audit** | Independent review | Different model critiques draft |

### 🎚️ Tiered Validation

| Tier | Time | Use Case |
|------|------|----------|
| 🟢 Notes | 30 min | Brainstorming, exploration |
| 🟡 Draft | 2-4 hrs | Advisor feedback, internal review |
| 🔴 Publication | 1-2 days | Journal submission |

### 🔄 Multi-Draft Support

Up to 5 iterations per project:
1. Submit draft → Agent review with comments
2. Revise → Submit v2 → New comments
3. Continue until satisfied
4. Version history preserved

---

## Deployment

### OpenClaw

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/weiaiwayne/commscribe.git
```

### Claude Code

```bash
curl -O https://raw.githubusercontent.com/weiaiwayne/commscribe/main/CLAUDE_BUNDLE.md
mv CLAUDE_BUNDLE.md CLAUDE.md
```

Or clone for full functionality:
```bash
git clone https://github.com/weiaiwayne/commscribe.git .commscribe
```

### Google Antigravity

```bash
cd ~/.gemini/antigravity/skills
git clone https://github.com/weiaiwayne/commscribe.git
cd commscribe && cp -r antigravity/* .
```

---

## Quick Test

After installation, try:

```
Write a literature review paragraph on networked gatekeeping
```

If working correctly, the assistant should:
- Ask for your research question and theoretical framing
- Ask if you have a voice profile (or offer to create one)
- Ask about your validation tier (Notes/Draft/Publication)
- Generate text that avoids AI patterns

If it produces "In recent years, gatekeeping has become increasingly important..." — the setup isn't working.

---

## Project Structure

```
commscribe/
├── README.md
├── CLAUDE_BUNDLE.md           # One-file version
├── skill-templates/
│   ├── SKILL.md               # Main entry point
│   ├── stages/                # 4-stage workflow
│   │   ├── concept.md
│   │   ├── synthesis.md
│   │   ├── drafting.md
│   │   └── audit.md
│   ├── voice/                 # Voice learning
│   │   ├── extraction.md      # Statistical extraction
│   │   ├── prompting.md       # Voice-constrained prompts
│   │   ├── adaptive.md        # AI-native learning ⭐ NEW
│   │   └── profiles/
│   ├── anti-ai/               # Pattern avoidance
│   │   ├── patterns.md
│   │   └── validation.md
│   └── workflows/             # Tiered validation, nudges
│       ├── tiered-validation.md
│       ├── nudge-system.md
│       └── reflection-checkpoints.md
├── scripts/
│   ├── voice_learning.py      # Statistical voice extraction
│   ├── adaptive_voice.py      # AI-native voice learning ⭐ NEW
│   ├── anti_ai_patterns.py
│   └── enhanced_pipeline_guardrails.py
└── antigravity/               # Google Antigravity version
```

---

## Voice Profile Setup

### Option 1: From Writing Samples

Provide 5-10 samples of your writing (500+ words each):
- Published papers
- Dissertation chapters
- Working drafts

```
/commscribe setup voice from samples
```

### Option 2: From Zotero

If you have papers you've written in Zotero:

```
/commscribe setup voice from zotero --collection "My Papers"
```

### Profile Output

```json
{
  "avg_sentence_length": 22.5,
  "sentence_length_std": 8.3,
  "vocabulary_richness": 0.42,
  "passive_voice_ratio": 0.18,
  "hedge_frequency": 1.2,
  "preferred_hedges": ["suggests", "indicates", "appears"],
  "preferred_transitions": ["however", "yet", "while"],
  "first_person_usage": 1.5,
  "citation_density": 2.3
}
```

---

## Integration with CommDAAF

CommScribe and CommDAAF work together:

```
Research Workflow
       │
       ├── Literature Review (CommScribe)
       │   └── Theory → Literature → Writing
       │
       ├── Data Analysis (CommDAAF)  
       │   └── Data → Methods → Results
       │
       └── Paper
           └── Introduction + Lit Review (CommScribe)
           └── Methods + Results (CommDAAF)
           └── Discussion (Both)
```

---

## Acknowledgments

- **[CommDAAF](https://github.com/weiaiwayne/commDAAF)** — Sister project, shared architecture
- **[DAAF](https://github.com/DAAF-Contribution-Community/daaf)** — Original framework
- **Prof. Wayne Xu** — Methods development
- **LampBotics AI Lab** — Development environment

---

## Contributing

Contributions welcome:
- New anti-AI patterns
- Voice extraction improvements
- Additional workflow stages
- Discipline-specific adaptations

---

## License

GNU General Public License v3.0 (GPL-3.0), same as CommDAAF.

---

## Citation

```bibtex
@software{commscribe,
  title={CommScribe: Literature Review & Theorization Framework},
  author={Xu, Wayne and LampBotics AI Lab},
  year={2026},
  url={https://github.com/weiaiwayne/commscribe},
  license={GPL-3.0},
  note={Experimental. Sister project to CommDAAF.}
}
```

---

*Write like yourself — not like an AI pretending to be you.*
