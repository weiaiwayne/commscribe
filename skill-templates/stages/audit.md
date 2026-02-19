---
name: independent-audit
description: Stage 4 - Critical review by independent agent
triggers:
  - audit draft
  - review my draft
  - critical review
  - final check
---

# Stage 4: Independent Audit

## Purpose

Fresh AI instance (different model) critically reviews your draft for logical coherence, argument strength, and remaining issues.

---

## Why Different Model?

**The problem:** The model that wrote your draft has blind spots—it's invested in its own output.

**The solution:** A different model with different training provides genuinely independent review.

| Drafting Model | Audit Model | Rationale |
|----------------|-------------|-----------|
| Claude Opus | GPT-4o | Different perspective |
| Claude Sonnet | Claude Opus | Higher capability |
| GPT-4o | Claude Opus | Different training |

---

## Audit Dimensions

### 1. Logical Coherence

**Questions:**
- Does the argument flow logically?
- Are transitions between sections smooth?
- Do claims follow from evidence?
- Are there logical gaps or jumps?

**Output:**
```
## Logical Coherence: 8/10

Strengths:
- Clear progression from classic → networked → algorithmic
- Each section builds on previous

Issues:
- Gap between paragraph 3 and 4 in Section 2
  → You claim algorithmic gatekeeping is "fundamentally different" but
     don't explain HOW it differs until 2 paragraphs later
- Conclusion introduces new claim not set up in body
  → "platforms as infrastructure" framing appears suddenly
```

### 2. Argument Strength

**Questions:**
- Is the central argument clear?
- Is evidence sufficient for claims?
- Are counterarguments addressed?
- Is the contribution claim justified?

**Output:**
```
## Argument Strength: 7/10

Central argument: Clear ✓
"Algorithmic curation represents a third phase distinct from editorial 
and networked gatekeeping"

Evidence assessment:
- Well-supported: Evolution narrative (strong citations)
- Weak support: "third phase" claim (needs more empirical grounding)
- Missing: Direct comparison showing algorithmic ≠ networked

Counterarguments:
- Not addressed: "Algorithms just amplify existing network patterns"
- Suggestion: Add paragraph acknowledging this critique (Bakshy et al. 2015)
```

### 3. Citation Accuracy

**Questions:**
- Are citations used correctly?
- Do cited claims match sources?
- Are any citations suspicious?
- Are [VERIFY] tags resolved?

**Output:**
```
## Citation Accuracy: 9/10

Spot-checked: 8 citations
- 7 appear accurate
- 1 flagged for verification:
  → "Gillespie (2018) argues platforms are 'necessarily political'" 
  → [CHECK: Is this quote accurate? Page number?]

[VERIFY] tags remaining: 2
- Meraz & Papacharissi quote on p.12
- Barzilai-Nahon mechanism typology

For Publication tier: Must resolve before submission
```

### 4. AI Pattern Check

**Questions:**
- Does the text sound AI-generated?
- Are banned patterns present?
- Is voice consistent with profile?

**Output:**
```
## AI Pattern Check: 9/10

Pattern density: 0.3/100 words (excellent)
Detected patterns: 1
- "Furthermore" in Section 3, paragraph 2
  → Suggestion: Replace with "Yet" or restructure

Voice consistency:
- Sentence length: Matches profile ✓
- Hedging: Slightly under-hedged in conclusion
- Transitions: Good variety ✓

Overall: Text does NOT read as AI-generated ✓
```

### 5. Structural Review

**Questions:**
- Is organization effective?
- Are sections balanced?
- Is anything missing?
- Is anything redundant?

**Output:**
```
## Structural Review: 8/10

Section balance:
- Introduction: 1,100 words (appropriate)
- Section 1 (Classic): 1,800 words (slightly long)
- Section 2 (Networked): 2,200 words (appropriate)
- Section 3 (Algorithmic): 2,400 words (appropriate)
- Discussion: 900 words (could expand)

Suggestions:
- Trim Section 1 by 300 words (well-trodden ground)
- Expand Discussion (implications underdeveloped)
- Consider combining paragraphs 4-5 in Section 2 (redundant)
```

---

## Audit Workflow

### Step 1: Submit for Audit

```
/commscribe audit draft

System: "Preparing independent audit...

Draft: DRAFT_FULL.md (8,400 words)
Audit model: GPT-4o (different from drafting model)
Validation tier: Publication

Running 5-dimension audit...
Estimated time: 2-3 minutes"
```

### Step 2: Receive Audit Report

```
📋 INDEPENDENT AUDIT REPORT

Overall Score: 8.2/10

| Dimension | Score | Status |
|-----------|-------|--------|
| Logical Coherence | 8/10 | Good |
| Argument Strength | 7/10 | Needs work |
| Citation Accuracy | 9/10 | Good |
| AI Pattern Check | 9/10 | Excellent |
| Structural Review | 8/10 | Good |

Critical Issues (must fix): 2
Major Suggestions: 4
Minor Suggestions: 7

View full report? (yes/summary only)
```

### Step 3: Address Issues

```
Critical issues:

1. [ARGUMENT] "Third phase" claim needs empirical grounding
   Location: Section 3, paragraph 1
   Suggestion: Add evidence from platform studies (Bucher 2018, 
   van Dijck 2013) showing algorithmic mechanisms differ from 
   network-based amplification

2. [LOGIC] Gap between "fundamentally different" claim and explanation
   Location: Section 2, paragraphs 3-4
   Suggestion: Insert transitional paragraph explaining the difference
   before diving into mechanisms

Address now? (yes/save for later/reject suggestion)
```

### Step 4: Re-audit (Optional)

After revisions:

```
/commscribe re-audit

System: "Running follow-up audit on revised draft...

Changes detected:
- Section 3 expanded (+320 words)
- New paragraph added in Section 2
- 'Furthermore' replaced with 'Yet'

Re-audit results:
| Dimension | Before | After |
|-----------|--------|-------|
| Argument Strength | 7/10 | 8/10 | ⬆️
| Logical Coherence | 8/10 | 9/10 | ⬆️
| AI Pattern Check | 9/10 | 10/10 | ⬆️

Critical issues resolved: 2/2 ✓
Ready for submission? (yes/continue revising)"
```

---

## Audit Report Format

Full audit report saved as:

```markdown
# Independent Audit Report

**Draft:** DRAFT_FULL.md
**Date:** 2026-02-19
**Audit Model:** GPT-4o
**Validation Tier:** Publication

## Executive Summary

Overall assessment: GOOD with minor revisions needed
Recommendation: Address critical issues, then ready for submission

## Detailed Findings

### 1. Logical Coherence (8/10)
[detailed findings]

### 2. Argument Strength (7/10)
[detailed findings]

### 3. Citation Accuracy (9/10)
[detailed findings]

### 4. AI Pattern Check (9/10)
[detailed findings]

### 5. Structural Review (8/10)
[detailed findings]

## Action Items

### Critical (Must Fix)
1. [description]
2. [description]

### Major (Should Fix)
1. [description]
...

### Minor (Consider)
1. [description]
...

## Revision Tracking

| Issue | Status | Resolution |
|-------|--------|------------|
| Third phase claim | Pending | — |
| Logic gap | Pending | — |
...
```

---

## Completion

After passing audit:

```
✅ AUDIT COMPLETE

Your draft has passed independent review.

Final checklist:
[x] Logical coherence verified
[x] Argument strength acceptable
[x] Citations spot-checked
[x] No AI patterns detected
[x] Structure approved

Output files:
- DRAFT_FINAL.md (clean version)
- AUDIT_REPORT.md (for your records)
- REVISION_LOG.md (changes made)

Ready for submission. Good luck! 🎓
```

---

*Every paper benefits from a skeptical reader. Let the audit be that reader.*
