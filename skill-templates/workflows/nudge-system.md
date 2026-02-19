---
name: nudge-system
description: Force conscious decisions in literature review process
triggers:
  - force choice
  - no defaults
  - conscious decision
---

# Nudge System for Literature Review

## Philosophy

> **"Every default embeds assumptions. Every shortcut has costs."**

CommScribe uses nudges to ensure you make conscious choices rather than sleepwalking through your literature review.

---

## Five Nudge Types

### 1. Default Danger Flags

**When triggered:** User accepts a default without consideration

**Example: Theoretical Framework**

```
User: "Just use whatever theory fits"

System: ⚠️ DEFAULT ALERT ⚠️

You're about to proceed WITHOUT explicit theoretical framing.

🚨 DANGER: This will produce a literature SUMMARY, not a REVIEW.

A literature review requires:
- Explicit theoretical lens guiding analysis
- Framework for organizing and critiquing sources
- Perspective that shapes your contribution

Without theory, you're just listing what others said.

Required: Choose your theoretical framing:

[ ] I have a framework (specify): ____________
[ ] I need help selecting one (system will suggest based on your topic)
[ ] I consciously choose atheoretical summary (NOT RECOMMENDED for publication)

Your choice: ___
```

### 2. Active Choice Requirement

**When triggered:** Binary or multi-way decision point

**Example: Scope Definition**

```
System: SCOPE DECISION REQUIRED

You must explicitly define boundaries. There is no "comprehensive" option.

Temporal scope:
[ ] Historical (pre-2010)
[ ] Contemporary (2010-present)
[ ] Focused period: _______ to _______
[ ] Full historical evolution

Platform scope:
[ ] Single platform: _______
[ ] Platform comparison: _______ vs _______
[ ] Platform-agnostic (general theory)

Geographic/linguistic scope:
[ ] Global (acknowledge Western bias)
[ ] Region-specific: _______
[ ] Explicitly Western platforms
[ ] Cross-cultural comparison

No default. You must choose each.
```

### 3. Trade-Off Visualization

**When triggered:** Decision with competing values

**Example: Depth vs. Breadth**

```
System: TRADE-OFF: Depth vs. Breadth

You can't have both. Choose your priority.

                    | Depth | Breadth | Time | Contribution |
--------------------|-------|---------|------|--------------|
Narrow deep dive    | ★★★★★ | ★☆☆☆☆   | High | Novel insight|
Broad survey        | ★★☆☆☆ | ★★★★★   | Med  | Overview     |
Focused synthesis   | ★★★★☆ | ★★★☆☆   | Med  | Integration  |
Selective critique  | ★★★★★ | ★★☆☆☆   | High | Challenge    |

Your concept suggests: Focused synthesis (theory integration)

Recommended: Focused synthesis
- Cover 3-4 theoretical streams
- Deep engagement with key papers
- Integration as contribution

Accept recommendation? (yes/choose different/explain options)
```

### 4. Assumption Audit

**When triggered:** Before major analysis decisions

**Example: Pre-Synthesis Audit**

```
System: 📋 ASSUMPTION AUDIT

Before synthesizing literature, check your assumptions:

1. "My search strategy captured relevant literature"
   Can you justify this? (y/n): ___
   If no: What might be missing? _______________

2. "My theoretical framing is appropriate for this topic"
   Can you justify this? (y/n): ___
   If no: What alternatives exist? _______________

3. "My scope boundaries are defensible"
   Can you justify this? (y/n): ___
   If no: What's the weakness? _______________

4. "I can fairly represent perspectives I disagree with"
   Can you justify this? (y/n): ___
   If no: What bias might affect synthesis? _______________

5. "My contribution claim is realistic"
   Can you justify this? (y/n): ___
   If no: Should you revise the claim? _______________

Assumptions not justified become acknowledged limitations.
```

### 5. Reflection Checkpoints

**When triggered:** At stage transitions

**Example: Post-Synthesis Reflection**

```
System: 🔄 REFLECTION CHECKPOINT

Before proceeding to drafting, reflect:

1. What patterns did you EXPECT to find in the literature?
   Expected: _________________________________

2. What did you ACTUALLY find?
   Found: _________________________________

3. What SURPRISED you?
   Surprise: _________________________________

4. How do you explain the surprise?
   Explanation: _________________________________

5. What ALTERNATIVE interpretations exist?
   Alternative 1: _________________________________
   Alternative 2: _________________________________

6. What would DISPROVE your synthesis?
   Falsifying evidence: _________________________________

⚠️ If you can't answer #5 and #6, you're not thinking critically.

Ready to proceed? (yes/need more reflection)
```

---

## Nudge Integration Points

| Stage | Nudge Type | Purpose |
|-------|-----------|---------|
| Concept | Default Danger | Theory selection |
| Concept | Active Choice | Scope definition |
| Concept | Trade-Off | Depth vs breadth |
| Synthesis | Assumption Audit | Pre-synthesis check |
| Synthesis | Reflection | Post-synthesis reflection |
| Drafting | Active Choice | Voice profile decision |
| Drafting | Default Danger | Citation handling |
| Audit | Reflection | Pre-submission reflection |

---

## Bypassing Nudges

For experienced researchers, nudges can be acknowledged quickly:

```
/commscribe expert mode

System: "Expert mode enabled.

Nudges will be condensed to single confirmations:
- 'Theory: networked gatekeeping. Confirm?' (y/n)
- 'Scope: Western platforms 2015-2025. Confirm?' (y/n)

Full nudges still triggered for:
- Publication tier validation
- Critical decision points
- First use of new features

Disable expert mode anytime with /commscribe standard mode"
```

---

## Decision Recording

All nudge responses are recorded:

```json
{
  "project_id": "gatekeeping_review_20260219",
  "decisions": [
    {
      "nudge": "theoretical_framework",
      "choice": "networked_gatekeeping",
      "justification": "Meraz & Papacharissi framework addresses...",
      "timestamp": "2026-02-19T10:30:00"
    },
    {
      "nudge": "scope_temporal",
      "choice": "2010-2025",
      "justification": "Post-algorithmic-feed era most relevant",
      "timestamp": "2026-02-19T10:32:00"
    }
  ]
}
```

**Use:** Auto-generate methods section from decisions.

---

## Methods Section Generator

```
/commscribe generate methods from decisions

System: "Generating methods section from recorded decisions...

## Methods

This review employs Meraz and Papacharissi's (2013) networked gatekeeping 
framework to analyze literature on algorithmic curation. The scope includes 
English-language scholarship on Western social media platforms (primarily 
Twitter and Facebook) from 2010-2025, with emphasis on post-algorithmic-feed 
literature (2016+).

Literature was identified through systematic search of [databases] using 
[queries], supplemented by backward citation tracking from key works. 
A total of [N] sources were included based on [criteria].

The review adopts a focused synthesis approach, prioritizing depth of 
engagement with theoretical contributions over comprehensive coverage.
Excluded from scope: [exclusions and justifications].

Limitations: [from assumption audit]

---

Generated from your recorded decisions. Edit as needed."
```

---

*Conscious choices make defensible methods. Sleepwalking makes reviewer #2 angry.*
