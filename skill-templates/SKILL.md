---
name: commscribe
description: Literature review & theorization framework with voice learning and anti-AI awareness
metadata:
  version: 0.1.0
  author: Wayne Xu / LampBotics AI Lab
  sister_project: commDAAF
---

# CommScribe — Literature Review & Theorization Framework

**Version 0.1.0** — Voice learning, anti-AI patterns, 4-stage workflow.

An OpenClaw skill package for academic writing and literature synthesis.

---

## Trigger Patterns

Activate this skill when user requests involve:
- "literature review on [topic]"
- "write about [theory/concept]"
- "synthesize research on [topic]"
- "theorize [phenomenon]"
- "draft a section on [topic]"
- "review my draft"
- "setup voice profile"
- "write in my voice"

---

## The 4-Stage Workflow

| Stage | You Have | You Want | Entry |
|-------|----------|----------|-------|
| **1️⃣ Concept** | Research idea | Validated concept plan | "start lit review on..." |
| **2️⃣ Synthesis** | Validated concept | Literature integration | "synthesize literature on..." |
| **3️⃣ Drafting** | Literature notes | Written draft | "draft section on..." |
| **4️⃣ Audit** | Complete draft | Critical review | "audit my draft" |

### Stage 1: Concept Planning (GATED)

**Validation Requirements:**
- Minimum 300 words
- At least 3 citations
- Clear research question
- Theoretical framing
- Original voice (not generic AI)

**If validation fails:** Return specific feedback, require revision.

### Stage 2: Literature Synthesis

**Search Methods:**
- Two-stage retrieval (keyword → semantic rerank)
- Three-path retrieval (keyword + embedding + domain)
- Hybrid search (Zotero KG + OpenAlex API)

**Output:** Integrated literature notes with citations.

### Stage 2.5: Voice Learning (Optional but Recommended)

**Extract voice profile from user's writing:**
- Sentence length patterns
- Vocabulary richness
- Hedging preferences
- Transition usage
- Citation integration style

**Sample Requirements:**
- 5-10 samples
- 500+ words each
- User's own writing

### Stage 3: Drafting (Voice-Constrained)

**Generation with voice profile:**
- Match sentence patterns
- Use preferred hedges/transitions
- Maintain vocabulary richness
- Avoid AI patterns (286 banned phrases)

**Multi-draft support:**
- Up to 5 iterations
- Agent comments on each
- Version history preserved

### Stage 4: Independent Audit

**Different model reviews:**
- Logical coherence
- Argument strength
- Citation accuracy
- AI pattern check
- Voice consistency

---

## Engagement Modes

### Concept Mode
**Triggers:** "start", "begin", "new literature review"

Validate research concept before proceeding.

### Synthesis Mode
**Triggers:** "synthesize", "search literature", "find papers"

Search and integrate literature.

### Drafting Mode
**Triggers:** "write", "draft", "compose"

Generate text in user's voice.

### Audit Mode
**Triggers:** "review", "audit", "critique my draft"

Critical review with actionable feedback.

### Voice Setup Mode
**Triggers:** "setup voice", "learn my style", "extract voice"

Create voice profile from samples.

---

## Anti-AI Pattern Enforcement

**286 patterns across 10 categories:**

1. **Generic Openers** — "In recent years", "With the rise of"
2. **Importance Phrases** — "It is important to note"
3. **Overused Transitions** — "Furthermore", "Moreover"
4. **Excessive Hedging** — "could potentially possibly"
5. **Filler Phrases** — "a wide range of"
6. **Structural Patterns** — "Let's dive in"
7. **Inflated Adjectives** — "groundbreaking", "transformative"
8. **Emoji/Symbols** — 🔑💡✨ in academic text
9. **Academic AI Patterns** — "This paper aims to fill a gap"
10. **Conclusion Clichés** — "In conclusion", "All in all"

**Enforcement:** Prompt-based instruction before generation.

---

## Tiered Validation

| Tier | Time | Use Case | Requirements |
|------|------|----------|--------------|
| 🟢 **Notes** | 30 min | Brainstorming | Minimal—exploration allowed |
| 🟡 **Draft** | 2-4 hrs | Advisor review | Citations required, [VERIFY] tags OK |
| 🔴 **Publication** | 1-2 days | Journal submission | Full verification, no [VERIFY] tags |

---

## Agent Invocation

```yaml
# Literature search (fast model)
sessions_spawn:
  task: "Search literature on {topic}"
  model: google/gemini-2.0-flash

# Synthesis (reasoning model)
sessions_spawn:
  task: "Synthesize {papers} into integrated review"
  model: anthropic/claude-sonnet-4-5

# Drafting (quality model)
sessions_spawn:
  task: "Draft section with voice profile: {profile}"
  model: anthropic/claude-opus-4-5

# Audit (DIFFERENT model than drafting)
sessions_spawn:
  task: "Critically audit this draft: {draft}"
  model: openai/gpt-4o
```

---

## Available Skills

### Stages
- `stages/concept.md` — Concept validation workflow
- `stages/synthesis.md` — Literature search & integration
- `stages/drafting.md` — Voice-constrained generation
- `stages/audit.md` — Independent critical review

### Voice Learning
- `voice/extraction.md` — Extract style from samples
- `voice/prompting.md` — Voice-constrained prompts
- `voice/profiles/` — Stored user profiles

### Anti-AI
- `anti-ai/patterns.md` — 286 patterns to avoid
- `anti-ai/validation.md` — Pattern density checking

### Workflows
- `workflows/tiered-validation.md` — Match rigor to stakes
- `workflows/nudge-system.md` — Force conscious choices
- `workflows/reflection-checkpoints.md` — Metacognition pauses

---

## Citation Integrity

### [VERIFY] Tag System

When uncertain about a citation:
```
Smith (2020) argues that gatekeeping has evolved [VERIFY: exact page number needed]
```

**Draft tier:** [VERIFY] tags allowed
**Publication tier:** All [VERIFY] tags must be resolved

### Citation Density Matching

Voice profile includes citation density:
- Extract from user's samples
- Match in generated text
- Flag if significantly different

---

## Human Checkpoints

Pause and notify at:
1. After concept validation (before synthesis)
2. After synthesis (before drafting)
3. After each draft iteration
4. Before final delivery

---

## Project Structure

```
project/
├── CONCEPT.md         # Validated concept plan
├── LITERATURE.md      # Synthesized notes
├── VOICE_PROFILE.json # User's voice profile
├── drafts/
│   ├── v1.md
│   ├── v2.md
│   └── v3.md
├── audit/
│   └── review.md
└── FINAL.md
```

---

## Quick Start

### New Literature Review

```
/commscribe start literature review on networked gatekeeping

→ System asks for concept plan
→ User provides concept (300+ words, 3+ citations)
→ System validates
→ Proceeds to synthesis
```

### Setup Voice Profile

```
/commscribe setup voice

→ System asks for 5-10 writing samples
→ User provides samples
→ System extracts profile
→ Profile saved for future use
```

### Draft with Voice

```
/commscribe draft introduction section

→ System loads voice profile
→ Generates in user's voice
→ Avoids AI patterns
→ Returns draft with comments
```

---

## Integration with CommDAAF

CommScribe handles writing; CommDAAF handles analysis.

**Shared components:**
- Tiered validation
- Nudge system
- Zotero integration
- Research integrity guardrails

**Handoff points:**
- CommDAAF results → CommScribe discussion section
- CommScribe literature → CommDAAF methodology framing

---

*Write like yourself — not like an AI pretending to be you.*
