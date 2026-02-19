---
name: tiered-validation
description: Match validation rigor to stakes
triggers:
  - validation tier
  - how thorough
  - notes vs draft vs publication
---

# Tiered Validation System

## Philosophy

> **"Validation should match your stakes, not a one-size-fits-all standard."**

Brainstorming notes don't need publication rigor. Journal submissions do.

---

## The Three Tiers

| Tier | Time | Stakes | Validation Level |
|------|------|--------|------------------|
| 🟢 **Notes** | 30-60 min | Exploration | Minimal |
| 🟡 **Draft** | 2-4 hours | Internal review | Standard |
| 🔴 **Publication** | 1-2 days | Journal submission | Rigorous |

---

## Tier Details

### 🟢 Notes Tier

**When to use:**
- Brainstorming ideas
- Exploring a new topic
- Personal reading notes
- Very early drafts

**What's allowed:**
- Speculative claims
- Missing citations
- [VERIFY] tags everywhere
- Rough organization
- AI-assisted exploration

**What's checked:**
- Basic coherence (does it make sense?)
- Nothing obviously wrong

**NOT checked:**
- Citation accuracy
- Voice matching
- AI pattern density
- Structural completeness

---

### 🟡 Draft Tier

**When to use:**
- Advisor/committee review
- Internal presentations
- Working papers
- Conference submissions (early stage)
- Dissertation chapter drafts

**What's required:**
- Citations for major claims
- Clear argument structure
- Reasonable organization

**What's allowed:**
- [VERIFY] tags (up to 5)
- Some rough edges
- Incomplete sections (marked)

**What's checked:**
- Logical coherence
- Citation presence (not full verification)
- Basic voice matching
- AI pattern scan (flag but don't block)

---

### 🔴 Publication Tier

**When to use:**
- Journal submission
- Final dissertation
- Book chapters
- Public reports
- Anything with your name on it permanently

**What's required:**
- All [VERIFY] tags resolved
- All citations verified
- Complete argument
- Polished prose
- Voice consistency
- Zero AI patterns

**What's checked:**
- Full independent audit (Stage 4)
- Citation spot-checking
- Voice profile matching
- AI pattern density (must be < 0.5/100 words)
- Structural completeness
- Argument strength

---

## Tier Selection

### At Project Start

```
/commscribe start literature review on gatekeeping

System: "What validation tier for this project?

🟢 Notes — Exploration, brainstorming (30-60 min validation)
🟡 Draft — Advisor review, working paper (2-4 hr validation)
🔴 Publication — Journal submission (1-2 day validation)

Your choice: ___"
```

### Changing Tiers

You can upgrade (but not downgrade without warning):

```
/commscribe upgrade to publication tier

System: "Upgrading from Draft → Publication tier.

New requirements:
- All [VERIFY] tags must be resolved (currently: 3)
- Full independent audit required
- AI pattern density must be < 0.5/100 words

Current status:
- [VERIFY] tags: 3 (need 0)
- Audit: Not yet run
- AI patterns: 0.4/100 words ✓

Ready to address requirements? (yes/stay at draft tier)"
```

---

## Validation Checklists

### 🟢 Notes Checklist

```
[ ] Text makes basic sense
[ ] Ideas are captured
[optional] Rough citations noted
```

### 🟡 Draft Checklist

```
[ ] Research question clear
[ ] Theoretical framing present
[ ] Major claims have citations
[ ] Argument structure logical
[ ] Sections complete (or marked incomplete)
[ ] [VERIFY] tags < 5
[ ] No glaring AI patterns
```

### 🔴 Publication Checklist

```
[ ] Research question explicit and refined
[ ] Theoretical framing well-developed
[ ] ALL claims cited
[ ] All citations verified
[ ] [VERIFY] tags = 0
[ ] Independent audit passed (8+/10)
[ ] AI pattern density < 0.5/100 words
[ ] Voice consistency confirmed
[ ] Structure approved
[ ] Argument strength verified
[ ] Counterarguments addressed
[ ] Limitations acknowledged
```

---

## Tier-Specific Prompts

### Notes Tier Generation

```
Generate exploratory notes on [topic].

This is NOTES tier:
- Be comprehensive in coverage
- Don't worry about perfect citations
- Use [VERIFY] tags liberally
- Explore tangents if interesting
- This is for brainstorming, not submission
```

### Draft Tier Generation

```
Generate draft section on [topic].

This is DRAFT tier:
- Provide citations for major claims
- Use [VERIFY] for uncertain citations
- Maintain clear argument structure
- Follow voice profile
- Avoid obvious AI patterns
```

### Publication Tier Generation

```
Generate publication-ready section on [topic].

This is PUBLICATION tier:
- Every claim must be cited
- No [VERIFY] tags allowed
- Strict voice profile adherence
- Zero tolerance for AI patterns
- Must pass independent audit
- Write as if submitting tomorrow
```

---

## Time Estimates

| Activity | Notes | Draft | Publication |
|----------|-------|-------|-------------|
| Concept validation | 10 min | 30 min | 1 hour |
| Literature synthesis | 30 min | 2 hours | 4 hours |
| Voice setup | Skip | 30 min | 1 hour |
| Drafting | 30 min | 2 hours | 4 hours |
| Self-review | 10 min | 1 hour | 2 hours |
| Independent audit | Skip | 30 min | 2 hours |
| Revisions | 10 min | 1 hour | 4 hours |
| **Total** | **~1.5 hr** | **~7 hr** | **~18 hr** |

---

## Tier Badges

Output includes tier badge:

```
🟢 NOTES TIER
This document is exploratory. Citations not verified.

🟡 DRAFT TIER  
This document is for internal review. Some citations marked [VERIFY].

🔴 PUBLICATION TIER
This document has passed full validation and independent audit.
```

---

*Match the rigor to the stakes. Don't over-validate brainstorming. Don't under-validate submissions.*
