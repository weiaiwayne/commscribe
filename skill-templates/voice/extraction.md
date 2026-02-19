---
name: voice-extraction
description: Extract writing style profile from user samples
triggers:
  - setup voice
  - learn my style
  - extract voice profile
  - analyze my writing
---

# Voice Extraction

## Purpose

Extract a comprehensive style profile from your writing samples so CommScribe can generate text in YOUR voice.

## When to Use

- Before your first literature review with CommScribe
- When you want to update your voice profile
- When writing for a different audience/publication

## Sample Requirements

| Requirement | Minimum | Recommended |
|-------------|---------|-------------|
| Number of samples | 5 | 10+ |
| Words per sample | 500 | 1000+ |
| Total words | 2,500 | 10,000+ |

**Best sources:**
- Your published papers
- Dissertation chapters
- Working drafts (in your voice)
- Conference papers

**Avoid:**
- Co-authored work (unless your sections are marked)
- Heavily edited work (editor's voice, not yours)
- Very old work (style may have changed)

## What Gets Extracted

### Lexical Features

| Feature | What It Measures |
|---------|------------------|
| Type-Token Ratio | Vocabulary diversity |
| Average word length | Complexity preference |
| Function word distribution | Content-independent style markers |
| Content word preferences | Domain vocabulary |

### Syntactic Features

| Feature | What It Measures |
|---------|------------------|
| Sentence length (mean) | Complexity preference |
| Sentence length (std) | Variation/rhythm |
| Passive voice ratio | Academic formality |
| Question frequency | Rhetorical style |

### Discourse Features

| Feature | What It Measures |
|---------|------------------|
| Hedge frequency | Certainty expression |
| Hedge types | Preferred uncertainty markers |
| Transition frequency | Explicit structure |
| Transition preferences | "However" vs "Furthermore" |
| Paragraph length | Chunking preference |

### Academic Features

| Feature | What It Measures |
|---------|------------------|
| Citation density | Integration style |
| First-person usage | Authorial presence |

## Usage

### From Text Files

```python
from voice_learning import StyleProfileExtractor

extractor = StyleProfileExtractor()
extractor.add_samples_from_files([
    Path("paper1.txt"),
    Path("paper2.txt"),
    Path("dissertation_ch3.txt"),
])

profile = extractor.extract_profile("wayne")
extractor.save_profile(Path("wayne_voice_profile.json"))
```

### From Pasted Text

```python
extractor = StyleProfileExtractor()
extractor.add_sample("""
Your first writing sample here...
At least 500 words...
""")
extractor.add_sample("""
Your second writing sample...
""")

profile = extractor.extract_profile("wayne")
```

### Interactive Setup

```
/commscribe setup voice

System: "I'll analyze your writing to extract your voice profile.
Please provide 5-10 samples of YOUR writing (500+ words each).

Option 1: Paste text directly
Option 2: Provide file paths
Option 3: Pull from Zotero collection

Which option?"
```

## Profile Output

```json
{
  "user_id": "wayne",
  "extracted_at": "2026-02-19T14:30:00",
  "sample_count": 7,
  "total_words": 8420,
  
  "type_token_ratio": 0.42,
  "avg_word_length": 5.2,
  "vocabulary_richness": 0.38,
  
  "avg_sentence_length": 22.5,
  "sentence_length_std": 8.3,
  "sentence_length_range": [8, 45],
  "passive_voice_ratio": 0.18,
  "question_frequency": 0.02,
  
  "hedge_frequency": 1.2,
  "hedge_types": ["suggests", "indicates", "appears", "may"],
  "transition_frequency": 0.8,
  "preferred_transitions": ["however", "yet", "while", "although"],
  "paragraph_length_avg": 165,
  "paragraph_length_std": 45,
  
  "citation_density": 2.3,
  "first_person_usage": 1.5,
  
  "style_description": "Writing style characterized by moderately complex sentences with high variation. Uses balanced active/passive voice with moderate hedging. Features rich vocabulary and strong authorial presence.",
  
  "generation_constraints": "VOICE CONSTRAINTS:\n1. Sentence length: Target 22 words (±8)..."
}
```

## Validation

After extraction, the system shows a summary:

```
📊 VOICE PROFILE EXTRACTED

Samples analyzed: 7
Total words: 8,420

Key characteristics:
• Sentence length: 22.5 words (high variation)
• Vocabulary: Rich (TTR: 0.42)
• Voice: Active-dominant (18% passive)
• Hedging: Moderate ("suggests", "indicates")
• First-person: Present (1.5/100 words)

Your preferred transitions: however, yet, while
Your preferred hedges: suggests, indicates, appears

Does this match how you see your writing? (yes/adjust)
```

## Updating Profile

Profiles can be updated as your style evolves:

```
/commscribe update voice --add-sample "new_paper.txt"
```

Or regenerated from scratch:

```
/commscribe setup voice --replace
```

## Storage

Profiles stored in:
- OpenClaw: `~/.openclaw/workspace/commscribe/voice_profiles/`
- Project-local: `./voice_profiles/`

---

*Your voice is your scholarly fingerprint. Let's capture it.*
