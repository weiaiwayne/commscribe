# CommScribe — Unblock Your Scholarship

**Version 0.1.0** | One-file bundle for Claude Code

*Your ideas. Your voice. We just help you get unstuck.*

Drop this file into your project as `CLAUDE.md` to enable CommScribe.

---

## What CommScribe Does NOT Do

- ❌ **Write your paper** — that's your job
- ❌ **Generate arguments** — ideas come from YOU
- ❌ **Replace reading** — you still read, we help organize
- ❌ **Work without input** — no samples = no voice = generic output

---

## The Problem

Every academic knows the feeling:
- **Blank page paralysis** — you know what to say, can't start
- **Literature overwhelm** — drowning in papers
- **Voice fatigue** — after hours of writing, you don't sound like yourself

These aren't signs you can't write. They're signs you're human.

---

## What CommScribe DOES

**Helps you get unstuck — while keeping YOUR voice at the center.**

- Pushes through mental blocks with structured workflows
- Handles busywork (lit search, organization) so you can think
- Learns YOUR voice, generates scaffolding in YOUR style
- Blocks 286 generic patterns that dilute your voice

Sister project to [CommDAAF](https://github.com/weiaiwayne/commDAAF) (data analysis).

---

## Trigger Patterns

Activate when user requests involve:
- "literature review on [topic]"
- "write about [theory/concept]"
- "draft a section on [topic]"
- "setup voice profile"
- "audit my draft"

---

## The 4-Stage Workflow

| Stage | Purpose | Gate |
|-------|---------|------|
| **1. Concept** | Validate research question | 300+ words, 3+ citations |
| **2. Synthesis** | Search & integrate literature | Zotero + API search |
| **3. Drafting** | Write in user's voice | Voice profile + anti-AI |
| **4. Audit** | Independent critical review | Different model reviews |

---

## Stage 1: Concept Validation

**Before proceeding, validate the concept plan.**

Requirements:
- Minimum 300 words
- At least 3 citations
- Clear research question
- Theoretical framing
- Original voice (not generic AI)

**Red flags to detect:**
- "This paper will explore..."
- "In recent years..."
- "fills a gap in the literature"

If detected: "Your concept sounds generic. Add specific details from your reading."

---

## Stage 2: Literature Synthesis

Search methods:
1. User's Zotero library (if connected)
2. OpenAlex API
3. Semantic Scholar API

Organize by themes from concept plan.
Generate synthesis notes with citations.
Flag gaps that support user's contribution.

---

## Stage 2.5: Voice Learning (Recommended)

Extract user's writing style from 5-10 samples (500+ words each).

**Statistical Mode (Traditional):**
- Sentence length (mean, std)
- Vocabulary richness (type-token ratio)
- Passive voice ratio
- Hedge frequency and types ("suggests", "indicates")
- Transition preferences ("however" vs "furthermore")
- First-person usage
- Citation density

**Adaptive Mode (AI-Native):**
- Embedding-based signature (captures gestalt)
- Feedback learning ("sounds like me" / "doesn't")
- Contrastive anchors (what voice is NOT)
- Calibrating threshold

**Output:** Voice profile JSON + generation constraints.

**User feedback loop:**
```
After generation, ask: "Does this sound like you?"
[👍 Yes] → Strengthen this direction
[👎 No]  → Push away from this style
```

---

## Stage 3: Voice-Constrained Drafting

**Every generation prompt must include:**

```
## VOICE CONSTRAINTS

[Insert user's voice profile here]

## ANTI-AI REQUIREMENTS (STRICTLY ENFORCED)

DO NOT USE these patterns:

GENERIC OPENERS:
- "In today's world/society/age"
- "In recent years"
- "With the rise of"
- "As we navigate"
- "It is no secret that"

IMPORTANCE PHRASES:
- "It is important to note that"
- "It is worth noting that"
- "It should be noted that"
- "Importantly," / "Notably," / "Crucially,"

OVERUSED TRANSITIONS:
- "Furthermore," / "Moreover," / "Additionally,"
- "In conclusion," / "To summarize,"
- "Firstly, ... Secondly, ... Thirdly,"

EXCESSIVE HEDGING:
- "could potentially"
- "might possibly"
- "may or may not"
- "one could argue that"

FILLER PHRASES:
- "a wide range of"
- "plays a crucial role in"
- "in terms of"
- "due to the fact that"

STRUCTURAL PATTERNS:
- "Let's dive in"
- "Here are [N] reasons"
- "The bottom line is"

INFLATED ADJECTIVES:
- "groundbreaking" / "revolutionary" / "transformative"
- "robust" / "comprehensive" / "holistic"
- "very" / "extremely" / "incredibly"

ACADEMIC AI PATTERNS:
- "This paper explores"
- "This study aims to"
- "fills a gap in the literature"
- "contributes to our understanding"
- "sheds light on"

CONCLUSION CLICHÉS:
- "In conclusion,"
- "All in all,"
- "At the end of the day,"
- "only time will tell"

EMOJI:
- No 🔑💡✨🎯🚀 in academic text

INSTEAD:
- Start with specific subjects, data, or claims
- Use concrete numbers ("40% increase" not "significant increase")
- Let logic connect ideas, not formulaic transitions
- Sound like the author of the examples
- Vary sentence length naturally
```

---

## Stage 4: Independent Audit

**Use DIFFERENT model than drafting.**

Audit dimensions:
1. Logical coherence (8/10 minimum)
2. Argument strength (7/10 minimum)
3. Citation accuracy (spot-check)
4. AI pattern density (<0.5/100 words)
5. Structural completeness

Provide actionable feedback with specific locations.

---

## Tiered Validation

| Tier | Use Case | Requirements |
|------|----------|--------------|
| 🟢 Notes | Brainstorming | Minimal |
| 🟡 Draft | Advisor review | Citations, [VERIFY] tags OK |
| 🔴 Publication | Journal submission | Full verification, audit passed |

Ask user which tier at project start.

---

## Nudge System

Force conscious decisions at key points:

1. **Default Danger Flags** — Warn about accepting defaults
2. **Active Choice Requirement** — Force explicit selection
3. **Trade-Off Visualization** — Show what you gain/lose
4. **Assumption Audit** — Surface hidden assumptions
5. **Reflection Checkpoints** — Pause for metacognition

---

## Project Structure

```
project/
├── CONCEPT.md           # Validated concept plan
├── LITERATURE.md        # Synthesized notes
├── VOICE_PROFILE.json   # User's voice profile
├── drafts/
│   ├── v1.md
│   └── v2.md
├── AUDIT_REPORT.md
└── FINAL.md
```

---

## Quick Reference

### Start New Review
```
/commscribe start literature review on [topic]
→ Ask for concept plan
→ Validate (300+ words, 3+ citations)
→ Proceed to synthesis
```

### Setup Voice
```
/commscribe setup voice
→ Ask for 5-10 writing samples
→ Extract style profile
→ Save for future use
```

### Draft Section
```
/commscribe draft [section]
→ Load voice profile
→ Load anti-AI constraints
→ Generate in user's voice
→ Provide quality report
```

### Audit Draft
```
/commscribe audit
→ Switch to different model
→ Run 5-dimension audit
→ Provide actionable feedback
```

---

## Zotero Integration

Connect your Zotero library for voice learning and citation management.

### Setup

```bash
# Set credentials (choose one method)

# Option 1: Environment variables
export ZOTERO_USER_ID="your_user_id"
export ZOTERO_API_KEY="your_api_key"

# Option 2: Config file
mkdir -p ~/.commscribe
cat > ~/.commscribe/zotero.json << EOF
{
  "user_id": "your_user_id",
  "api_key": "your_api_key"
}
EOF
```

Get your credentials at [zotero.org/settings/keys](https://www.zotero.org/settings/keys)

### Features

**Voice Learning from Your Papers**
```
Pull writing samples from Zotero
→ Gets solo-authored papers (pure voice)
→ Extracts abstracts for style analysis
→ Builds voice profile
```

**Literature Search**
```
Search user's library for: [query]
→ Searches title, abstract, tags
→ Returns matching papers with citations
→ Prioritizes user's existing knowledge
```

**Citation Verification**
```
Verify: "Meraz & Papacharissi (2013)"
→ Matches against library
→ Returns full citation info
→ Flags if not in library
```

### In Your Workflow

When user says "setup voice from my papers":
1. Connect to Zotero
2. Get solo-authored or first-authored papers
3. Extract abstracts/text
4. Build voice profile

When user says "search my library":
1. Query user's Zotero
2. Return relevant citations
3. Note gaps for external search

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

## Citation

```bibtex
@software{commscribe,
  title={CommScribe: Literature Review & Theorization Framework},
  author={Xu, Wayne and LampBotics AI Lab},
  year={2026},
  url={https://github.com/weiaiwayne/commscribe}
}
```

---

*Write like yourself — not like an AI pretending to be you.*
