# CommScribe

**Scholarly Authenticity Framework** | v0.1.0

*The Anti-AI AI — helps you NOT sound like you used AI.*

**Sister project to [CommDAAF](https://github.com/weiaiwayne/commDAAF)** — while CommDAAF handles data analysis, CommScribe handles literature review, theory building, and scholarly writing.

---

## ⚠️ Experimental Software

This framework is under active development at the [LampBotics AI Lab](https://lampbotics.com). Use with caution.

---

## What This Is NOT

❌ A shortcut to academic writing  
❌ An AI ghostwriter  
❌ A way to "generate" scholarship  
❌ A replacement for thinking  

**You can write. CommScribe isn't here because you can't.**

---

## The Real Problem

Scholars face a paradox:

1. **Literature review is tedious busywork** — hours of searching, organizing, synthesizing that could be spent *thinking*
2. **Time pressure produces generic prose** — when exhausted, everyone sounds the same
3. **AI tools make it worse** — they make it *too easy* to sound like generic academic-ese
4. **Your voice drifts** — across papers, under deadlines, your distinctive style erodes

The result? Work that sounds like it could have been written by anyone. Or worse — sounds like it was written by ChatGPT.

---

## What CommScribe Actually Does

**Protects your scholarly identity.**

| Problem | CommScribe Solution |
|---------|---------------------|
| Tedious lit review | Automates search & organization, frees you to *think* |
| Voice drift | Learns YOUR style, enforces it in every draft |
| AI-sounding prose | Actively blocks 286 patterns that signal AI generation |
| Generic writing | Matches YOUR sentence rhythms, hedging style, transitions |
| Citation chaos | Integrates with YOUR Zotero, maintains YOUR density |

**The goal:** Text that sounds exactly like you wrote it — because the ideas ARE yours, and now the prose is too.

---

## The Anti-AI Principle

Here's the irony: CommScribe uses AI to help you *not sound like AI*.

Most AI writing tools optimize for fluency. CommScribe optimizes for **authenticity**:
- Learns what makes YOUR writing distinctive
- Flags and blocks generic AI patterns
- Matches your voice profile, not "academic writing" in general
- Provides independent audit to catch drift

If someone can tell you used AI, CommScribe failed.

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
