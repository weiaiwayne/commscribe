---
name: voice-prompting
description: Generate voice-constrained prompts for drafting
triggers:
  - write in my voice
  - use my style
  - voice-constrained generation
---

# Voice-Constrained Prompting

## Purpose

Convert a voice profile into effective prompts that constrain LLM generation to match your writing style.

---

## Prompt Architecture

### Three-Tier Structure

```
┌─────────────────────────────────────┐
│ TIER 1: Voice Characterization      │
│ (Human-readable style description)  │
├─────────────────────────────────────┤
│ TIER 2: Generation Constraints      │
│ (Specific numeric targets)          │
├─────────────────────────────────────┤
│ TIER 3: Anti-AI Patterns            │
│ (What NOT to do)                    │
├─────────────────────────────────────┤
│ TIER 4: Few-Shot Examples           │
│ (Excerpts from user's writing)      │
└─────────────────────────────────────┘
```

---

## Tier 1: Voice Characterization

Human-readable description of writing style:

```
## VOICE CHARACTERIZATION

Writing style characterized by moderately complex sentences (22.5 words avg) 
with high variation (±8.3). Uses balanced active/passive voice (18% passive) 
with moderate hedging. Features rich vocabulary (TTR: 0.42) and strong 
authorial presence (frequent I/we).

Key characteristics:
- Sentences vary from short punchy (12 words) to long complex (35 words)
- Prefers "suggests" and "indicates" over "proves" or "demonstrates"
- Uses "however" and "yet" rather than "furthermore" or "moreover"
- Integrates citations mid-sentence, not just at end
- First-person singular for claims, plural for field consensus
```

---

## Tier 2: Generation Constraints

Specific, measurable targets:

```
## GENERATION CONSTRAINTS

1. SENTENCE LENGTH
   - Target: 22 words (±8)
   - Range: 14-30 words
   - Vary deliberately: mix short and long

2. PARAGRAPH LENGTH
   - Target: 165 words
   - Range: 120-210 words

3. PASSIVE VOICE
   - Target: 18% of sentences
   - Use for: objectivity, emphasis on action over actor

4. HEDGING
   - Frequency: ~1.2 per 100 words
   - Preferred: "suggests", "indicates", "appears", "may"
   - Avoid: "proves", "demonstrates", "clearly shows"

5. TRANSITIONS
   - Preferred: "however", "yet", "while", "although"
   - Avoid: "furthermore", "moreover", "additionally"

6. FIRST PERSON
   - Frequency: ~1.5 per 100 words
   - "I argue" for personal claims
   - "We see" for field consensus

7. CITATIONS
   - Density: ~2.3 per 100 words
   - Integration: mid-sentence preferred
   - Style: "Smith (2020) argues..." not "...is important (Smith, 2020)"
```

---

## Tier 3: Anti-AI Patterns

Explicit prohibitions:

```
## ANTI-AI REQUIREMENTS (STRICTLY ENFORCED)

### NEVER USE:

OPENERS:
❌ "In recent years"
❌ "In today's world"
❌ "With the rise of"
❌ "As we navigate"

IMPORTANCE MARKERS:
❌ "It is important to note that"
❌ "It is worth noting that"
❌ "Importantly,"
❌ "Notably,"

TRANSITIONS:
❌ "Furthermore,"
❌ "Moreover,"
❌ "Additionally,"
❌ "In conclusion,"

HEDGES:
❌ "could potentially"
❌ "might possibly"
❌ "may or may not"

FILLER:
❌ "a wide range of"
❌ "plays a crucial role"
❌ "in terms of"

ACADEMIC CLICHÉS:
❌ "This paper explores"
❌ "fills a gap"
❌ "sheds light on"

### INSTEAD:

✅ Start with specific subjects, dates, claims
✅ Show importance through evidence, not announcement
✅ Use "but", "and", "yet", "so" for transitions
✅ Be direct about uncertainty
✅ Cut filler—get to the point
✅ State your contribution specifically
```

---

## Tier 4: Few-Shot Examples

Excerpts from user's actual writing:

```
## WRITING EXAMPLES (Match this voice)

### Example 1 (Introduction style):
"Algorithmic feeds have fundamentally restructured how information flows 
through digital media systems. Where editorial gatekeepers once determined 
what publics would see, platform algorithms now curate personalized streams 
based on engagement predictions (Gillespie, 2018). This shift raises a 
critical question..."

### Example 2 (Argument style):
"I argue that algorithmic curation represents a third phase in gatekeeping's 
evolution—neither the centralized control of editorial gatekeeping nor the 
distributed agency of networked gatekeeping, but a hybrid form where platform 
infrastructure shapes what networked actors can amplify."

### Example 3 (Literature engagement style):
"While Benkler et al. (2018) focused on network structure, and Vosoughi et 
al. (2018) examined spread speed, neither addresses how platform design 
choices create differential amplification. This gap motivates the present 
review."

---
Match the voice, rhythm, and style of these examples.
```

---

## Complete Prompt Template

```
{TIER 1: Voice Characterization}

{TIER 2: Generation Constraints}

{TIER 3: Anti-AI Patterns}

{TIER 4: Few-Shot Examples}

---

## WRITING TASK

{User's request here}

---

## INSTRUCTIONS

Write the above content as if you ARE the author of the examples.

Requirements:
1. Match sentence length patterns (22 ± 8 words)
2. Use the specified hedging and transition preferences
3. Maintain vocabulary richness
4. STRICTLY avoid all anti-AI patterns
5. Integrate citations as shown in examples
6. Sound like a specific person, not generic academic

Begin writing:
```

---

## Generating Prompts Programmatically

```python
from voice_learning import VoicePromptGenerator, StyleProfile

# Load profile
profile = StyleProfile.from_json("wayne_voice_profile.json")

# Load samples for few-shot
samples = [
    Path("paper1.txt").read_text()[:1000],
    Path("paper2.txt").read_text()[:1000],
]

# Create generator
generator = VoicePromptGenerator(profile, samples)

# Generate full prompt
voice_prompt = generator.generate_voice_prompt(
    include_examples=True,
    include_anti_ai=True
)

# Wrap with task
full_prompt = generator.wrap_generation_request(
    content_request="Write an introduction section on networked gatekeeping",
    voice_prompt=voice_prompt
)

# Send to LLM
response = llm.generate(full_prompt)
```

---

## Validation After Generation

Check that output matches profile:

```python
from voice_learning import StyleProfileExtractor
from anti_ai_patterns import get_pattern_density, check_text_for_patterns

# Extract style from generated text
extractor = StyleProfileExtractor()
extractor.add_sample(generated_text)
output_profile = extractor.extract_profile("generated")

# Compare to target
print(f"Sentence length: {output_profile.avg_sentence_length} (target: {profile.avg_sentence_length})")
print(f"Passive voice: {output_profile.passive_voice_ratio} (target: {profile.passive_voice_ratio})")

# Check AI patterns
density = get_pattern_density(generated_text)
print(f"AI pattern density: {density}/100 words (target: <0.5)")

if density > 1.0:
    matches = check_text_for_patterns(generated_text)
    print("Detected patterns:", matches)
```

---

*The prompt is the control surface. Tune it to produce your voice.*
