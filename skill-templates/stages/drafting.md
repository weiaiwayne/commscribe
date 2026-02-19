---
name: voice-constrained-drafting
description: Stage 3 - Generate draft in user's voice with anti-AI awareness
triggers:
  - draft section
  - write in my voice
  - generate draft
  - compose
---

# Stage 3: Voice-Constrained Drafting

## Purpose

Generate literature review text in YOUR voice while avoiding AI-detectable patterns.

---

## Prerequisites

Before drafting, you should have:

| Requirement | Source |
|-------------|--------|
| Validated concept | Stage 1 |
| Synthesized literature | Stage 2 |
| Voice profile | Stage 2.5 (recommended) |

---

## Voice Injection

### With Voice Profile

If you have a voice profile, drafting uses:

```
## VOICE CHARACTERIZATION

Writing style characterized by moderately complex sentences (22.5 words avg)
with high variation (±8.3). Uses balanced active/passive voice with moderate 
hedging. Features rich vocabulary (TTR: 0.42) and strong authorial presence.

Key features:
- Sentence length: 22.5 words (std: 8.3)
- Passive voice: 18%
- Hedging frequency: 1.2 per 100 words
- Preferred hedges: suggests, indicates, appears
- Preferred transitions: however, yet, while
- First-person usage: 1.5 per 100 words

## GENERATION CONSTRAINTS

1. Sentence length: Target 22 words (±8), vary between 14-30
2. Paragraph length: ~165 words
3. Use hedges like "suggests, indicates" every ~80 words
4. Prefer "however, yet, while" over "furthermore, moreover"
5. Avoid all patterns in the anti-AI list
```

### Without Voice Profile

Uses conservative academic defaults with emphasis on anti-AI patterns:

```
## DEFAULT ACADEMIC VOICE

- Moderate sentence length (18-25 words)
- Balanced active/passive
- Standard hedging
- STRICT anti-AI pattern avoidance
```

---

## Anti-AI Integration

Every drafting prompt includes:

```
## ANTI-AI REQUIREMENTS (STRICTLY ENFORCED)

- NEVER use: "In recent years", "It is important to note", "Furthermore"
- NEVER use: "a wide range of", "plays a crucial role"
- NEVER conclude with: "In conclusion", "To summarize"
- NO emoji in academic text
- NO numbered lists unless explicitly requested

INSTEAD:
- Start sentences with specific subjects, data, claims
- Use concrete numbers and examples
- Let logic connect ideas, not formulaic transitions
- Sound like the author of the examples, not generic academic-ese
```

---

## Drafting Workflow

### Step 1: Section Selection

```
/commscribe draft introduction

System: "Drafting introduction based on:
- Concept plan: CONCEPT.md
- Literature synthesis: LITERATURE.md
- Voice profile: wayne_voice_profile.json

Estimated length: 800-1200 words
Include: Research question, theoretical framing, contribution claim

Proceed? (yes/adjust parameters)"
```

### Step 2: Generation

```
Generating draft...
- Loading voice constraints
- Loading anti-AI patterns (286)
- Structuring from synthesis notes
- Writing in characterized voice

Draft generated: 1,050 words
```

### Step 3: Review & Comments

System provides inline comments:

```markdown
## Introduction

Algorithmic feeds have fundamentally restructured how information flows through
digital media systems. [COMMENT: Strong opening—specific claim, no generic opener ✓]

Where editorial gatekeepers once determined what publics would see, platform 
algorithms now curate personalized streams based on engagement predictions
(Gillespie, 2018). [COMMENT: Good citation integration ✓]

This shift raises a critical question: How has algorithmic curation changed 
the distribution of gatekeeping power? [COMMENT: Research question clear ✓]

...

Drawing on Meraz and Papacharissi's (2013) networked gatekeeping framework,
I argue that algorithmic curation represents a third phase in gatekeeping's
evolution—neither the centralized control of editorial gatekeeping nor the
distributed agency of networked gatekeeping, but a hybrid form where platform
infrastructure shapes what networked actors can amplify.
[COMMENT: Theoretical framing present, contribution claim clear ✓]
```

### Step 4: Quality Check

```
📊 DRAFT QUALITY CHECK

Voice matching:
- Sentence length: 21.3 (target: 22.5) ✓
- Vocabulary richness: 0.39 (target: 0.42) ✓
- Passive voice: 15% (target: 18%) ✓
- Hedge frequency: 1.0 (target: 1.2) ⚠️ slightly low

Anti-AI patterns:
- Patterns detected: 0 ✓
- Pattern density: 0.2/100 words ✓

Citation integrity:
- Citations: 8
- [VERIFY] tags: 1
- Density: 2.1/100 words (target: 2.3) ✓

Overall: ✅ GOOD — Minor hedge adjustment suggested
```

---

## Multi-Draft Iteration

### Draft Versioning

Up to 5 drafts per section:

```
project/drafts/
├── introduction_v1.md
├── introduction_v1_comments.md
├── introduction_v2.md
├── introduction_v2_comments.md
└── introduction_v3.md  # current
```

### Revision Workflow

```
/commscribe submit revision

System: "Comparing v2 → v3...

Changes detected:
- Paragraph 2 rewritten (was 120 words, now 95)
- Citation added: Bucher 2018
- Transition changed: 'Furthermore' → 'Yet'

Running quality check on v3...

✅ Improvements:
- Removed 1 AI pattern ('Furthermore')
- Better voice match in paragraph 2

⚠️ Concerns:
- Paragraph 3 now has 3 sentences starting with 'This'
- Consider varying sentence openings

Submit v3 as current? (yes/revise more)"
```

### Requesting Specific Changes

```
/commscribe revise paragraph 3 to vary sentence openings

System: "Revising paragraph 3...

Original:
'This framework extends... This extension allows... This approach differs...'

Revised:
'The framework extends... By incorporating algorithmic actors, the extension 
allows... Unlike prior approaches, this one differs...'

Accept revision? (yes/adjust/reject)"
```

---

## Section Types

### Introduction
- Research question
- Theoretical framing
- Contribution claim
- Roadmap (optional)

### Literature Review Body
- Thematic organization
- Synthesis (not summary)
- Tensions and debates
- Gaps leading to contribution

### Discussion/Conclusion
- Summary of argument
- Implications
- Limitations
- Future directions

---

## Output

Stage 3 produces:

```
project/
├── CONCEPT.md
├── LITERATURE.md
├── drafts/
│   ├── introduction_v1.md
│   ├── literature_review_v1.md
│   └── discussion_v1.md
├── DRAFT_FULL.md        # Compiled draft
└── QUALITY_REPORT.md    # Voice + anti-AI metrics
```

---

## Proceeding to Stage 4

When satisfied with draft:

```
/commscribe ready for audit

System: "Preparing for Stage 4: Independent Audit

Current draft:
- Total words: 8,400
- Sections: 4
- Citations: 42
- [VERIFY] tags remaining: 3

Pre-audit checklist:
[ ] All sections complete
[ ] [VERIFY] tags acceptable for your tier
[ ] Ready for critical review by different model

Proceed to audit? (yes/revise more)"
```

---

*Your voice, your ideas, your paper—just faster.*
