---
name: concept-validation
description: Stage 1 - Validate research concept before proceeding
triggers:
  - start literature review
  - new review
  - concept plan
  - research question
---

# Stage 1: Concept Planning

## Purpose

Validate that your research concept is sufficiently developed before investing time in literature synthesis. Prevents wasted effort on poorly conceived projects.

---

## Validation Gate

**Your concept plan MUST include:**

| Requirement | Minimum | Why It Matters |
|-------------|---------|----------------|
| Word count | 300 words | Demonstrates sufficient engagement |
| Citations | 3 references | Shows grounded knowledge |
| Research question | Explicit | Defines scope and contribution |
| Theoretical framing | Present | Provides analytical lens |
| Original voice | Detected | Not generic AI output |

---

## What to Submit

A concept plan should address:

### 1. Research Question
What specific question are you answering?

**❌ Too vague:** "How does social media affect politics?"
**✅ Specific:** "How do algorithmic feeds amplify partisan content compared to chronological feeds?"

### 2. Theoretical Framing
What theory guides your analysis?

**❌ Missing:** "I'll look at gatekeeping."
**✅ Present:** "Drawing on Meraz and Papacharissi's (2013) networked gatekeeping framework, I examine how algorithmic curation redistributes gatekeeping power from editors to platforms."

### 3. Literature Context
What existing work does this build on or challenge?

**❌ Generic:** "Many scholars have studied this."
**✅ Specific:** "While Benkler et al. (2018) focused on network structure, and Vosoughi et al. (2018) examined spread speed, neither addresses how platform design choices create differential amplification."

### 4. Contribution Claim
What's new about your approach?

**❌ Vague:** "This fills a gap."
**✅ Specific:** "By comparing algorithmic vs. chronological conditions in the same platform (Twitter's 2016 transition), I isolate the algorithmic effect from confounding platform differences."

### 5. Scope Boundaries
What are you NOT covering?

**Example:** "This review focuses on English-language research on Western platforms; Chinese social media and non-democratic contexts are outside scope."

---

## Validation Process

### Step 1: Submit Concept

```
User: /commscribe start literature review on networked gatekeeping

System: "Please provide your concept plan (300+ words).

Include:
1. Your research question
2. Theoretical framing
3. Key literature you're building on
4. Your contribution claim
5. Scope boundaries"
```

### Step 2: Automated Checks

```python
from enhanced_pipeline_guardrails import ConceptValidator

validator = ConceptValidator()
assessment = validator.assess(concept_text)

# Returns:
# - has_research_question: bool
# - has_theoretical_framing: bool
# - has_literature_grounding: bool
# - has_original_voice: bool
# - word_count: int
# - citation_count: int
# - depth_score: float
# - can_proceed: bool
# - feedback: List[str]
```

### Step 3: Feedback

**If validation passes:**
```
✅ CONCEPT VALIDATED

- Word count: 450 ✓
- Citations: 5 ✓
- Research question: Clear ✓
- Theoretical framing: Present ✓
- Original voice: Detected ✓

Ready to proceed to Stage 2 (Literature Synthesis).
```

**If validation fails:**
```
⚠️ CONCEPT NEEDS REVISION

Issues found:
- ❌ No clear research question detected
- ❌ Insufficient citations (1 found, need 3+)
- ⚠️ Theoretical framing is vague

Suggestions:
- State your research question explicitly: "This review asks..."
- Add 2+ more citations to key works in your area
- Name your theoretical framework: "Drawing on [theory]..."

Please revise and resubmit.
```

---

## Red Flag Detection

The system flags generic AI-sounding phrases:

| Red Flag | Why It's a Problem |
|----------|-------------------|
| "This paper will explore..." | Generic opener |
| "In recent years..." | Filler, not specific |
| "With the rise of..." | Cliché |
| "The purpose of this research is to..." | Formulaic |
| "fills a gap in the literature" | Overused claim |

**If detected:** "Your concept sounds generic. Use specific details from your reading to establish your voice."

---

## Depth Score

Beyond the checklist, we calculate a depth score (0-1):

**Depth indicators:**
- Nuance markers: "however", "although", "yet"
- Critical thinking: "gap", "limitation", "critique"
- Engagement: "argues", "suggests", "contends"
- Theory: "framework", "lens", "perspective"
- Methodology: "method", "approach", "analysis"

**Target:** depth_score ≥ 0.4

---

## Example: Passing Concept

```markdown
## Research Question

How has algorithmic curation changed the distribution of gatekeeping power 
in hybrid media systems? Specifically, I ask: What mechanisms allow 
algorithmic feeds to amplify certain voices while suppressing others, 
and how does this differ from editorial gatekeeping?

## Theoretical Framing

I draw on Meraz and Papacharissi's (2013) networked gatekeeping framework, 
which extends Shoemaker and Vos's (2009) gatekeeping theory to account for 
distributed, non-hierarchical information flows. However, their framework 
predates the widespread adoption of algorithmic feeds. I extend their 
typology to include "algorithmic gatekeepers"—platform-level systems that 
curate without human editorial judgment.

## Literature Context

Three streams of research inform this review:

1. **Classic gatekeeping** (White 1950; Shoemaker & Vos 2009): Editors as 
   gatekeepers selecting what publics see.

2. **Networked gatekeeping** (Meraz & Papacharissi 2013; Barzilai-Nahon 2008): 
   Power distributed across network nodes, not concentrated in editors.

3. **Algorithmic curation** (Gillespie 2018; Bucher 2018): Platforms as 
   infrastructural gatekeepers with opaque selection criteria.

What's missing: Integration of these streams into a unified framework that 
explains how algorithmic and human gatekeeping interact in hybrid systems.

## Contribution

This review synthesizes gatekeeping evolution from editorial → networked → 
algorithmic, proposing a multi-level framework that accounts for:
- Individual-level sharing decisions
- Network-level amplification patterns  
- Platform-level algorithmic curation

## Scope

Focus: English-language scholarship on Western platforms (Twitter, Facebook).
Excluded: Chinese platforms (different regulatory context), broadcast media.
Timeframe: 2010-2025, emphasizing post-algorithmic-feed literature (2016+).
```

**Assessment:** ✅ PASSES (520 words, 7 citations, clear RQ, strong framing)

---

## Proceeding to Stage 2

Once validated, the concept plan is saved and used to:
1. Guide literature search queries
2. Frame synthesis structure
3. Maintain focus throughout drafting

```
Concept validated. Saving to project/CONCEPT.md

Proceeding to Stage 2: Literature Synthesis
→ Search queries will be generated from your research question
→ Results will be filtered by your scope boundaries
→ Synthesis will follow your theoretical framing
```

---

*A strong concept is the foundation of a strong review.*
