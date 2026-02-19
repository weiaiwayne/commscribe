---
name: anti-ai-patterns
description: Comprehensive catalog of AI writing patterns to avoid
triggers:
  - avoid ai patterns
  - write naturally
  - human-like writing
  - anti-detection
---

# Anti-AI Pattern Awareness

## Philosophy

> **"AI-generated text has a fingerprint. CommScribe teaches you to avoid leaving it."**

AI detectors like GPTZero, Originality.ai, and Turnitin identify AI text through statistical patterns. CommScribe instructs the LLM to avoid these patterns at generation time.

---

## Pattern Categories

### 1. Generic Openers (23 patterns)

**❌ AVOID:**
- "In today's [world/society/age]"
- "In recent years"
- "In the realm of"
- "Throughout history"
- "As we navigate"
- "With the rise of"
- "Given the importance of"
- "When it comes to"
- "It is no secret that"

**✅ INSTEAD:**
- Start with specific subjects, dates, or claims
- "Twitter's 2016 algorithmic feed changed..."
- "Meraz and Papacharissi (2013) argue..."
- "Three mechanisms drive amplification..."

---

### 2. Importance/Noting Phrases (20 patterns)

**❌ AVOID:**
- "It is important to note that"
- "It is worth noting that"
- "It should be noted that"
- "It is crucial to understand that"
- "It cannot be overstated that"
- "Importantly,"
- "Notably,"
- "Crucially,"

**✅ INSTEAD:**
- Just state the thing. If it's important, show why.
- "Gatekeeping has evolved—editors no longer control distribution."
- "This limitation undermines causal claims."

---

### 3. Overused Transitions (28 patterns)

**❌ AVOID:**
- "Furthermore,"
- "Moreover,"
- "Additionally,"
- "Consequently,"
- "In conclusion,"
- "To summarize,"
- "First and foremost,"
- "Last but not least,"
- "Firstly, ... Secondly, ... Thirdly,"

**✅ INSTEAD:**
- Use simpler connectors: "but", "and", "yet", "so"
- Let logic connect ideas without announcing
- "This approach also addresses..." not "Additionally, this approach..."

---

### 4. Excessive Hedging (23 patterns)

**❌ AVOID:**
- "may or may not"
- "could potentially"
- "might possibly"
- "to some extent"
- "in certain respects"
- "it would seem that"
- "one could argue that"

**✅ INSTEAD:**
- Be direct about uncertainty
- "We don't know whether..."
- "Evidence is mixed on..."
- "This suggests X, though Y remains unclear."

---

### 5. Filler Phrases (40 patterns)

**❌ AVOID:**
- "a wide range of"
- "a variety of"
- "a plethora of"
- "plays a crucial role in"
- "serves as"
- "in terms of"
- "with regard to"
- "due to the fact that"

**✅ INSTEAD:**
- Cut the filler. Get to the point.
- "Three factors matter" not "A wide range of factors play a crucial role"
- "Because users vary" not "Due to the fact that users have various preferences"

---

### 6. Structural Patterns (26 patterns)

**❌ AVOID:**
- "Let's dive in"
- "Let's explore"
- "Let's unpack"
- "Great question!"
- "Here's the thing:"
- "The bottom line is"
- "Here are [N] reasons/ways/tips"

**✅ INSTEAD:**
- Write as a scholar, not a content creator
- State findings directly
- No listicle energy in academic writing

---

### 7. Inflated Adjectives (36 patterns)

**❌ AVOID:**
- "very", "really", "extremely"
- "groundbreaking"
- "revolutionary"
- "transformative"
- "cutting-edge"
- "robust" (overused in AI)
- "comprehensive" (overused)
- "novel" (when everything is "novel")

**✅ INSTEAD:**
- Use precise descriptors
- "This approach improves precision by 40%" not "This is a groundbreaking approach"
- Show, don't inflate

---

### 8. Emoji and Symbols (23 patterns)

**❌ AVOID in academic writing:**
- 🔑 💡 ✨ 🎯 🚀 ⭐ 📊 ✅ ❌
- Excessive em-dashes (3+ per paragraph)
- Arrows in prose (→)
- Bullets in flowing text

**✅ INSTEAD:**
- Use words
- Reserve symbols for actual diagrams/figures

---

### 9. Academic AI Patterns (38 patterns)

**❌ AVOID:**
- "This paper explores"
- "This study aims to"
- "fills a gap in the literature"
- "contributes to our understanding of"
- "sheds light on"
- "provides insights into"
- "the findings suggest that"
- "future research should"

**✅ INSTEAD:**
- Be specific about your contribution
- "Prior work assumes X; we show Y"
- "Smith (2020) focused on A; we extend to B"
- "The effect size (d=0.4) matches lab studies"

---

### 10. Conclusion Clichés (29 patterns)

**❌ AVOID:**
- "In conclusion,"
- "To conclude,"
- "In summary,"
- "All in all,"
- "At the end of the day,"
- "only time will tell"
- "remains to be seen"

**✅ INSTEAD:**
- Conclude with substance, not announcement
- State implications directly
- "Algorithmic gatekeeping concentrates power differently than editorial gatekeeping—but power still concentrates."

---

## Implementation

CommScribe injects anti-AI awareness into every generation prompt:

```
## ANTI-AI REQUIREMENTS (STRICTLY ENFORCED)

- NEVER use phrases from the banned patterns list
- NEVER start paragraphs with "In recent years", "It is important to note"
- NEVER use "Furthermore, Moreover, Additionally" in sequence
- NEVER conclude with "In conclusion" or "To summarize"
- NO emoji in academic text
- NO numbered lists unless explicitly requested

INSTEAD:
- Start with specific subjects, data, or claims
- Use concrete numbers and examples
- Let ideas connect logically
- Sound like a specific person, not generic academic-ese
```

---

## Pattern Density Check

After generation, check pattern density:

```python
from anti_ai_patterns import get_pattern_density, check_text_for_patterns

density = get_pattern_density(generated_text)
# Human text: < 1.0 per 100 words
# AI text: > 3.0 per 100 words

if density > 1.5:
    print("⚠️ Text may still sound AI-generated")
    matches = check_text_for_patterns(generated_text)
    # Returns which patterns were found
```

---

## Research Foundation

Based on:
- Kumar et al. (2023) "Can AI-Generated Text be Reliably Detected?"
- Wang et al. (2023) "SeqXGPT: Sentence-Level AI-Generated Text Detection"
- Liang et al. (2024) "Mapping the Increasing Use of LLMs in Scientific Papers"
- Community observations from AI detection discourse

---

*The best way to avoid AI detection is to not write like AI.*
