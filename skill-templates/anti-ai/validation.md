---
name: anti-ai-validation
description: Check text for AI patterns and validate humanization
triggers:
  - check ai patterns
  - validate text
  - pattern density
---

# Anti-AI Validation

## Purpose

Check generated text for AI-detectable patterns and validate that it passes humanization standards.

---

## Pattern Density Metric

**Definition:** AI patterns per 100 words

| Density | Interpretation |
|---------|----------------|
| < 0.5 | Excellent — indistinguishable from human |
| 0.5 - 1.0 | Good — minor patterns, likely passes detection |
| 1.0 - 2.0 | Caution — some patterns, may flag detectors |
| 2.0 - 3.0 | Poor — noticeable AI patterns |
| > 3.0 | Bad — clearly AI-generated |

**Target for CommScribe:** < 0.5 per 100 words

---

## Validation Workflow

### Step 1: Pattern Scan

```python
from anti_ai_patterns import check_text_for_patterns, get_pattern_density

text = """Your generated text here..."""

# Get overall density
density = get_pattern_density(text)
print(f"Pattern density: {density:.2f}/100 words")

# Get specific matches
matches = check_text_for_patterns(text)
for category, patterns in matches.items():
    print(f"\n{category}:")
    for pattern in patterns:
        print(f"  ❌ {pattern}")
```

### Step 2: Category Breakdown

```
📊 AI PATTERN ANALYSIS

Overall density: 0.8/100 words

By category:
├── Generic Openers: 0 found ✓
├── Importance Phrases: 1 found
│   └── "It is worth noting that" (line 23)
├── Overused Transitions: 2 found
│   ├── "Furthermore" (line 45)
│   └── "Moreover" (line 67)
├── Excessive Hedging: 0 found ✓
├── Filler Phrases: 0 found ✓
├── Structural Patterns: 0 found ✓
├── Inflated Adjectives: 1 found
│   └── "groundbreaking" (line 12)
├── Emoji/Symbols: 0 found ✓
├── Academic AI Patterns: 0 found ✓
└── Conclusion Clichés: 0 found ✓

Total patterns: 4
Density: 0.8/100 words

Verdict: ⚠️ GOOD but needs minor fixes
```

### Step 3: Fix Suggestions

```
🔧 SUGGESTED FIXES

1. Line 12: "groundbreaking"
   Current: "This groundbreaking approach..."
   Suggested: "This approach differs by..."
   
2. Line 23: "It is worth noting that"
   Current: "It is worth noting that algorithms..."
   Suggested: "Algorithms..." (just state it)

3. Line 45: "Furthermore"
   Current: "Furthermore, the findings indicate..."
   Suggested: "The findings also indicate..." or restructure

4. Line 67: "Moreover"
   Current: "Moreover, this pattern..."
   Suggested: "This pattern also..." or use "Yet"

Apply all fixes? (yes/select/manual)
```

---

## Automated Humanization

### Light Touch (Preserve meaning, fix patterns)

```python
from anti_ai_patterns import light_humanize

fixed_text = light_humanize(text)
# Replaces detected patterns with alternatives
# Preserves sentence structure and meaning
```

### Full Rewrite (Request regeneration with stricter constraints)

```
Pattern density too high (2.3/100 words).

Options:
1. Apply automated fixes (may affect flow)
2. Regenerate with stricter anti-AI prompt
3. Manual revision (show me the patterns)

Your choice: ___
```

---

## Validation Thresholds by Tier

| Tier | Max Density | Action if Exceeded |
|------|-------------|-------------------|
| 🟢 Notes | 3.0 | Warn only |
| 🟡 Draft | 1.5 | Suggest fixes |
| 🔴 Publication | 0.5 | Block + require fixes |

---

## Pre-Submission Check

For Publication tier, run full validation:

```
/commscribe validate for submission

System: "Running publication-tier validation...

1. Pattern density: 0.3/100 words ✓
2. Voice consistency: 92% match ✓
3. Citation density: 2.1/100 words (target: 2.3) ✓
4. [VERIFY] tags: 0 ✓
5. Sentence length variance: High ✓

✅ PASSED — Text is publication-ready

No AI patterns detected.
Voice matches profile.
Ready for submission."
```

---

## Comparison Testing

Compare against AI detectors (informational only):

```
/commscribe test against detectors

System: "⚠️ NOTE: This sends text to external services.

Testing against:
- GPTZero (simulated)
- Perplexity analysis (local)

Results:
- Estimated perplexity: 45.2 (human range: 30-60)
- Burstiness score: 0.72 (human range: 0.6-0.9)
- Sentence variance: High (human-like)

Assessment: Text characteristics fall within human writing range.

Disclaimer: Actual detector results may vary. This is indicative only."
```

---

## Continuous Monitoring

During drafting, patterns are monitored in real-time:

```
[Generating paragraph 3...]

⚠️ Pattern detected: "Furthermore" 
   Auto-replaced with: "Yet"

[Generating paragraph 4...]

✓ No patterns detected

[Generating paragraph 5...]

⚠️ Pattern detected: "It is important to note"
   Auto-replaced with: [sentence restructured]

Generation complete.
Patterns caught: 2
Patterns in final text: 0
Density: 0.2/100 words ✓
```

---

## Pattern Database Updates

The pattern database can be extended:

```python
from anti_ai_patterns import add_custom_pattern

# Add discipline-specific AI pattern
add_custom_pattern(
    category="Academic AI Patterns",
    pattern="as per the literature",
    example_bad="As per the literature, this is common",
    example_good="This pattern is common in the literature"
)
```

---

## Validation Report

Full report for audit:

```markdown
# Anti-AI Validation Report

**Document:** DRAFT_FINAL.md
**Date:** 2026-02-19
**Tier:** Publication

## Summary

| Metric | Value | Target | Status |
|--------|-------|--------|--------|
| Pattern density | 0.3/100 | <0.5 | ✅ Pass |
| Patterns found | 0 | 0 | ✅ Pass |
| Voice match | 94% | >90% | ✅ Pass |

## Category Breakdown

| Category | Count |
|----------|-------|
| Generic Openers | 0 |
| Importance Phrases | 0 |
| Overused Transitions | 0 |
| ... | ... |

## Conclusion

Text passes all anti-AI validation checks and is suitable for publication.

---
Generated by CommScribe v0.1.0
```

---

*Detection is a cat-and-mouse game. Stay ahead by not writing like AI in the first place.*
