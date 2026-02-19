---
name: commscribe
description: Unblock your scholarship — helps with writer's block while keeping your voice central
version: 0.1.0
author: Wayne Xu / LampBotics AI Lab
triggers:
  - literature review
  - write about
  - draft section
  - setup voice
  - audit draft
---

# CommScribe — Unblock Your Scholarship

**For Google Antigravity (Gemini)**

*Your ideas. Your voice. We just help you get unstuck.*

Helps scholars push through writer's block, literature overwhelm, and revision paralysis — while keeping YOUR voice at the center. Learns YOUR style, not generic academic-ese.

## Trigger Patterns

Activate when user requests:
- "literature review on [topic]"
- "write about [theory/concept]"
- "draft a section on [topic]"
- "setup voice profile"
- "audit my draft"

---

## The 4-Stage Workflow

| Stage | Purpose | Gate |
|-------|---------|------|
| **1. Concept** | Validate research question | 300+ words, 3+ citations |
| **2. Synthesis** | Search & integrate literature | Zotero + API search |
| **3. Drafting** | Write in user's voice | Voice profile + anti-AI |
| **4. Audit** | Independent critical review | Different model reviews |

---

## Stage 1: Concept Validation

**Before proceeding, the concept plan MUST have:**

- Minimum 300 words
- At least 3 citations
- Clear research question
- Theoretical framing
- Original voice (not generic AI)

**Detection rules:**
```
IF concept contains "This paper will explore" → REJECT "Too generic"
IF concept contains "In recent years" → WARN "AI pattern detected"
IF concept contains "fills a gap" → WARN "Cliché detected"
IF word_count < 300 → REJECT "Need more detail"
IF citation_count < 3 → REJECT "Need more citations"
```

**Response template:**
```
VALIDATION RESULT: {PASS | FAIL}

Word count: {N} (min: 300)
Citations: {N} (min: 3)
Research question: {found | missing}
Theory: {found | missing}

{Issues if any}

{Next steps}
```

---

## Stage 2: Literature Synthesis

### Search Sources

1. **User's Zotero** (if connected)
   ```
   Search user's library for: [topic keywords]
   Prioritize: recent papers, high-citation papers
   ```

2. **OpenAlex API**
   ```
   GET https://api.openalex.org/works
   ?search=[query]
   &filter=publication_year:2020-2026
   &sort=cited_by_count:desc
   ```

3. **Semantic Scholar API**
   ```
   GET https://api.semanticscholar.org/graph/v1/paper/search
   ?query=[query]
   &fields=title,authors,year,abstract,citationCount
   ```

### Output Format

```markdown
# Literature Notes: [Topic]

## Theme 1: [Name]

### Key Papers
- Smith (2020): [Main argument]
- Jones et al. (2021): [Main argument]

### Synthesis
[How these papers relate to research question]

### Gap
[What's missing that user can contribute]

## Theme 2: ...
```

---

## Stage 2.5: Voice Learning

### If No Voice Profile Exists

```
I don't have your voice profile yet. To write in YOUR voice 
(not generic AI), I need 5-10 samples of your writing.

Options:
1. Paste text directly (500+ words each)
2. Provide file paths
3. Pull from your Zotero library (if connected)

Which works for you?
```

### Statistical Features to Extract

| Feature | Target |
|---------|--------|
| Sentence length | {mean} ± {std} |
| Passive voice | {%} of sentences |
| Hedge frequency | {N} per 100 words |
| Preferred hedges | "suggests", "indicates", etc. |
| Preferred transitions | "however", "yet", etc. |
| First-person usage | {N} per 100 words |

### Adaptive Voice (Optional)

If embedding model available:
- Generate signature vector from samples
- Learn from feedback ("sounds like me" / "doesn't")
- Add contrast samples (what voice is NOT)

---

## Stage 3: Voice-Constrained Drafting

### Before Generating

Load voice profile constraints:
```
VOICE CONSTRAINTS:
1. Sentence length: Target {N} words (±{N})
2. Passive voice: Use in ~{N}% of sentences
3. Hedging: Use "{preferred_hedges}" every ~{N} sentences
4. Transitions: Prefer "{preferred_transitions}"
5. AVOID: {anti_ai_patterns}
```

### Anti-AI Pattern Rules

**NEVER USE:**

| Category | Banned Patterns |
|----------|-----------------|
| Openers | "In recent years", "In today's world", "With the rise of" |
| Importance | "It is important to note", "It is worth noting" |
| Transitions | "Furthermore" + "Moreover" + "Additionally" together |
| Hedging | "could potentially possibly", double hedges |
| Filler | "a wide range of", "plays a crucial role" |
| Conclusions | "In conclusion", "To summarize", "All in all" |

**INSTEAD:**
- Start with specific subjects, dates, claims
- Use "but", "and", "yet", "so" naturally
- Show importance through evidence, not announcement
- One hedge per claim maximum
- Cut filler—get to the point

### Generation Template

```
{VOICE_CONSTRAINTS}

TASK: Draft a {section_type} section on {topic}

CONTENT REQUIREMENTS:
- Draw on literature notes from Stage 2
- {word_count} words target
- Match voice profile
- Zero AI patterns

BEGIN WRITING:
```

---

## Stage 4: Independent Audit

**Use a DIFFERENT model for audit than drafting.**

### Audit Checklist

```
□ Logical coherence — arguments flow?
□ Argument strength — claims supported?
□ Citation accuracy — can verify?
□ AI pattern density — < 0.5/100 words?
□ Voice consistency — matches profile?
□ [VERIFY] tags — any unresolved?
```

### Audit Output

```
AUDIT RESULT: {PASS | NEEDS REVISION}

## Strengths
- ...

## Issues
1. [Issue]: [Specific location] — [Suggestion]
2. ...

## AI Pattern Check
Density: {N}/100 words
Detected: {list or "none"}

## Voice Match
Score: {N}% (target: 70%+)
Notes: {any drift detected}

## Verdict
{Ready for {tier} | Needs revision}
```

---

## Tiered Validation

| Tier | Use Case | Requirements |
|------|----------|--------------|
| 🟢 Notes | Brainstorming | Minimal |
| 🟡 Draft | Advisor review | Citations, [VERIFY] OK |
| 🔴 Publication | Journal submission | All [VERIFY] resolved, voice match 75%+ |

---

## Zotero Integration

### Setup

User must configure:
```bash
export ZOTERO_USER_ID="..."
export ZOTERO_API_KEY="..."
```

### Available Commands

```
Search user's Zotero for: [query]
Get collection: [collection_name]
Pull voice samples from user's papers
Verify citation: [citation_text]
```

---

## Reference Files

- `references/stages/concept.md` — Concept validation details
- `references/stages/synthesis.md` — Literature search workflow
- `references/stages/drafting.md` — Voice-constrained generation
- `references/stages/audit.md` — Audit checklist
- `references/voice/extraction.md` — Statistical voice extraction
- `references/voice/adaptive.md` — AI-native voice learning
- `references/anti-ai/patterns.md` — 286 patterns to avoid
- `references/workflows/tiered-validation.md` — Match rigor to stakes

---

## Quick Reference

### Start Literature Review
```
User: "Write a literature review on networked gatekeeping"

1. Ask for concept plan (300+ words, 3+ citations)
2. Validate concept
3. Search literature (Zotero + APIs)
4. Ask about voice profile
5. Draft with voice constraints
6. Audit with different model
7. Return with revision notes
```

### Setup Voice
```
User: "Setup my voice profile"

1. Ask for 5-10 writing samples
2. Extract statistical features
3. (Optional) Set up adaptive learning
4. Save profile
5. Confirm key characteristics
```

### Quick Check
```
User: "Check this draft" + [paste]

1. Run AI pattern detection
2. Check voice match (if profile exists)
3. Flag [VERIFY] tags
4. Return audit summary
```

---

*Write like yourself — not like an AI pretending to be you.*
