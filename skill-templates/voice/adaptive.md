---
name: adaptive-voice
description: AI-native voice learning that improves with feedback
triggers:
  - learn my voice
  - adaptive voice
  - teach you my style
  - voice feedback
---

# Adaptive Voice Learning

## The AI Way

Traditional voice extraction counts words and measures averages.  
Adaptive voice learning **understands the gestalt**.

| Traditional | Adaptive |
|-------------|----------|
| Counts sentence lengths | Captures sentence rhythm |
| Lists hedge words | Learns hedging style |
| Measures passive % | Feels the formality |
| Static profile | Improves with feedback |

---

## How It Works

### 1. Embedding-Based Learning

Instead of counting features, we embed your writing samples into a high-dimensional space where similar writing styles cluster together.

```
Your samples → Embeddings → Voice Signature (dense vector)
```

The signature captures the **holistic feel** of your writing.

### 2. Contrastive Learning

We also learn what your voice is NOT by contrasting against:
- Generic academic writing
- AI-generated text
- Other styles you don't want

```python
manager.add_contrast(ai_samples, "ai_generated")
manager.add_contrast(generic_samples, "generic_academic")
```

### 3. Feedback Loop

The system improves as you use it:

```
"Does this sound like you?"

[👍 Yes] → Pulls signature toward this style
[👎 No]  → Pushes signature away from this style
```

Over time, the threshold calibrates to YOUR preferences.

---

## Setup Flow

### Interactive (Recommended)

```
Agent: "I'll learn your writing voice. I need 5-10 samples of YOUR writing 
       (500+ words each). These should be solo-authored—your voice, not 
       a collaborator's.

       Options:
       1. Paste text directly
       2. Give me file paths
       3. Pull from your Zotero library

       Which works best?"

User: "Pull from Zotero"

Agent: "I see 722 items in your library. I'll look for solo-authored papers.
       Found 12 papers where you're the only author. Want me to use those?"

User: "Yes"

Agent: [Processes samples]

       "✅ Voice signature created!
       
       Learned from: 12 papers (28,400 words)
       Confidence: 85%
       
       Key characteristics I detected:
       • Medium-length sentences with high variation
       • Active voice dominant, strategic passive
       • Moderate hedging ('suggests', 'indicates')
       • Strong authorial presence (uses 'I' and 'we')
       
       Want me to also learn what your voice ISN'T?
       I can contrast against AI-generated text to avoid those patterns."

User: "Yes, do that"

Agent: [Adds AI contrast]

       "Done. I'll now actively avoid AI-typical patterns when writing 
       in your voice. Ready to start your literature review?"
```

### Programmatic

```python
from adaptive_voice import VoiceManager

manager = VoiceManager()

# Learn from samples
signature = manager.setup_voice(
    user_id="wayne",
    samples=[paper1_text, paper2_text, ...],
    contrast_samples={
        "ai_generated": [chatgpt_sample, ...],
        "generic_academic": [textbook_sample, ...]
    }
)

# Later: add more samples
manager.add_samples("wayne", [new_paper_text])
```

---

## Feedback Learning

### During Drafting

After generating text, the agent asks:

```
Agent: [Generated paragraph]

       "Does this sound like you? 
       [👍 Yes] [👎 No] [🤷 Skip]"

User: 👎

Agent: "Got it. What's off?
       [A] Too formal  [B] Too casual
       [C] Wrong rhythm [D] AI-sounding
       [E] Other"

User: "D"

Agent: "Thanks—I'll push away from AI patterns. Let me try again..."
```

### Batch Feedback

Review multiple outputs:

```
Agent: "Here are 3 versions. Rank them by how much they sound like you:

       Version A: [excerpt]
       Version B: [excerpt]  
       Version C: [excerpt]"

User: "B > A > C"

Agent: "Noted. I'll pull toward B's style and away from C's."
```

---

## Evaluation

Check any text against your voice:

```python
result = manager.evaluate("wayne", generated_text)

print(result)
# {
#   "similarity": 0.847,
#   "sounds_like_me": True,
#   "threshold": 0.75,
#   "confidence": 0.92,
#   "contrast_scores": {
#     "ai_generated": 0.23,
#     "generic_academic": 0.41
#   }
# }
```

### Similarity Score

- **> 0.85**: Very close match
- **0.70-0.85**: Good match
- **0.55-0.70**: Partial match
- **< 0.55**: Doesn't sound like you

### Contrast Scores

Lower = better. High contrast scores mean the text resembles the "bad" examples.

---

## Comparison Mode

Compare two drafts:

```python
result = manager.compare_texts(
    "wayne",
    text_a="First version of the paragraph...",
    text_b="Second version of the paragraph..."
)

print(result)
# {
#   "text_a_similarity": 0.82,
#   "text_b_similarity": 0.71,
#   "closer_to_voice": "a",
#   "difference": 0.11
# }
```

---

## Prompt Generation

Get a voice-constrained prompt for any LLM:

```python
prompt = manager.get_prompt("wayne")
```

Output:

```
## VOICE SIGNATURE

You are writing in a specific person's voice. This voice has been learned from 
12 samples (28,400 words total).

The voice signature has a confidence level of 92%.

## WHAT THIS VOICE IS NOT

This voice has been contrasted against:
ai_generated, generic_academic

Actively avoid characteristics of these contrast categories.

## VOICE EXEMPLARS

Study these examples carefully...

[Examples from user's writing]

## LEARNED FROM FEEDBACK

This voice profile has been refined through 47 feedback instances.
```

---

## Profile Evolution

Your voice profile improves over time:

```
Initial setup (12 samples)
├── Confidence: 72%
├── Threshold: 0.65
└── Feedback: 0

After 1 week of use
├── Confidence: 85%
├── Threshold: 0.71 (calibrated)
├── Feedback: 23 (+18/-5)
└── Added: 3 new samples

After 1 month
├── Confidence: 94%
├── Threshold: 0.74 (stable)
├── Feedback: 89 (+71/-18)
└── Contrasts: ai_generated, generic_academic, textbook_style
```

---

## Storage

Profiles saved to:
```
~/.commscribe/voices/
├── wayne.json           # Your voice signature
├── wayne_samples/       # Cached sample excerpts
└── wayne_history.jsonl  # Feedback history
```

---

## Integration with Pipeline

### Stage 3 (Drafting)

```python
# Load voice
manager = VoiceManager()
manager.load_voice("wayne")

# Generate with voice constraint
prompt = f"""
{manager.get_prompt("wayne")}

## TASK
Write a literature review section on networked gatekeeping...
"""

response = llm.generate(prompt)

# Evaluate result
eval = manager.evaluate("wayne", response)
if not eval["sounds_like_me"]:
    # Regenerate with stronger constraints
    ...
```

### Stage 4 (Audit)

```python
# Voice check in audit
eval = manager.evaluate("wayne", final_draft)

if eval["similarity"] < 0.7:
    warnings.append("⚠️ Voice drift detected - review for authenticity")

if eval["contrast_scores"].get("ai_generated", 0) > 0.5:
    warnings.append("⚠️ High AI-pattern similarity - humanize text")
```

---

## Tips

### Better Samples = Better Voice

- **Use solo-authored work** (not collaborative)
- **Use recent work** (style evolves)
- **Use similar genres** (conference paper voice ≠ grant proposal voice)
- **Minimum 5 samples, 500 words each**

### Feedback Quality Matters

- **Be honest** - don't approve text that "sounds okay but not like me"
- **Be specific** - "too formal" is better than "no"
- **Be consistent** - your feedback trains the model

### Multiple Voices

You can have different voice profiles:

```python
manager.setup_voice("wayne_academic", academic_samples)
manager.setup_voice("wayne_public", blog_samples)
manager.setup_voice("wayne_grants", grant_samples)
```

---

*The more you use it, the more it sounds like you.*
