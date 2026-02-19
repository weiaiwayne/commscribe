# CommScribe OpenClaw Integration

## Multi-Agent Workflow

CommScribe uses different models for different stages to maximize both speed and quality.

### Recommended Model Assignments

| Stage | Task | Model | Why |
|-------|------|-------|-----|
| **Synthesis** | Literature search | `google/gemini-2.0-flash` | Fast, good at retrieval |
| **Drafting** | Voice-constrained writing | `anthropic/claude-opus-4-5` | Best creative writing |
| **Audit** | Critical review | `openai/gpt-4o` | Different perspective |
| **Voice Setup** | Extract profile | `anthropic/claude-sonnet-4-5` | Good balance |

### Using sessions_spawn

For background processing, use OpenClaw's `sessions_spawn`:

```yaml
# Literature Synthesis (fast)
sessions_spawn:
  task: |
    Search and synthesize literature on "networked gatekeeping".
    Use OpenAlex and Semantic Scholar APIs.
    Return structured notes with citations.
  model: google/gemini-2.0-flash
  runTimeoutSeconds: 300

# Voice-Constrained Drafting (quality)
sessions_spawn:
  task: |
    Draft an introduction section on networked gatekeeping.
    Use voice profile: /path/to/wayne_voice_profile.json
    Follow anti-AI pattern guidelines.
    Target: 800-1000 words.
  model: anthropic/claude-opus-4-5
  runTimeoutSeconds: 600

# Independent Audit (different model)
sessions_spawn:
  task: |
    Critically audit this draft for:
    1. Logical coherence and argument strength
    2. Citation accuracy and integration
    3. AI pattern density (flag if > 0.5/100 words)
    4. Voice consistency with profile
    Return actionable feedback.
  model: openai/gpt-4o
  runTimeoutSeconds: 300
```

### Cron Jobs for Long-Running Tasks

For literature reviews that need periodic updates:

```yaml
# Daily literature check
cron:
  add:
    job:
      name: "commscribe-lit-check"
      schedule:
        kind: cron
        expr: "0 6 * * *"  # 6 AM daily
        tz: "America/New_York"
      sessionTarget: isolated
      payload:
        kind: agentTurn
        message: |
          Check for new papers on "algorithmic gatekeeping" published 
          in the last 24 hours. Add to LITERATURE.md if relevant.
        model: google/gemini-2.0-flash
```

### Session Workflow Example

Full literature review as a session:

```python
# In your main session, orchestrate the workflow:

# 1. Validate concept
validation = validate_concept(concept_text)
if not validation.passed:
    return f"Concept needs revision: {validation.issues}"

# 2. Spawn synthesis agent
sessions_spawn(
    task=f"Synthesize literature on: {research_question}",
    model="google/gemini-2.0-flash",
    label="synthesis-agent"
)
# Agent will ping back when done

# 3. When synthesis complete, spawn drafting agent
sessions_spawn(
    task=f"Draft introduction using synthesis notes and voice profile",
    model="anthropic/claude-opus-4-5",
    label="drafting-agent"
)

# 4. When draft complete, spawn audit agent
sessions_spawn(
    task=f"Audit this draft: {draft_text}",
    model="openai/gpt-4o", 
    label="audit-agent"
)
```

### Voice Profile Integration

Store voice profiles in OpenClaw workspace:

```
~/.openclaw/workspace/commscribe/
├── voice_profiles/
│   ├── wayne.json
│   └── wayne_samples/    # Source excerpts
├── projects/
│   └── gatekeeping-review/
│       ├── CONCEPT.md
│       ├── LITERATURE.md
│       └── drafts/
```

### Anti-AI Pattern Enforcement

Add to your OpenClaw system prompt:

```markdown
## CommScribe Anti-AI Guidelines

When generating academic text, NEVER use:
- "In recent years" / "In today's world"
- "It is important to note that"
- "Furthermore, Moreover, Additionally" (overused)
- "a wide range of" / "plays a crucial role"
- "In conclusion" / "To summarize"

Instead:
- Start with specific subjects, dates, claims
- Use "but", "and", "yet", "so" for transitions
- Show importance through evidence, not announcement
```

### Validation Gates in Workflow

```python
# Before proceeding to next stage, validate:

from commscribe.scripts.validation import validate_concept, validate_draft

# After concept submission
concept_result = validate_concept(concept_text)
if not concept_result.passed:
    # Return feedback, don't proceed
    message(f"❌ Concept needs work:\n{concept_result}")
    return

# After draft submission  
draft_result = validate_draft(
    draft_text,
    tier="publication",
    voice_match_score=0.78  # From adaptive voice evaluation
)
if not draft_result.passed:
    message(f"❌ Draft not ready for {tier}:\n{draft_result}")
    return
```

---

## Quick Reference

### Start Literature Review

```
/commscribe start lit review on [topic]
```

1. System asks for 300+ word concept with 3+ citations
2. Validates concept before proceeding
3. Spawns synthesis agent
4. Notifies when synthesis ready
5. Asks if ready to draft
6. Spawns drafting agent with voice profile
7. Returns draft with audit comments

### Setup Voice Profile

```
/commscribe setup voice
```

1. Asks for 5-10 writing samples
2. Offers: paste text / file paths / Zotero pull
3. Extracts statistical + adaptive profile
4. Asks if wants contrast samples (AI text)
5. Saves profile for future use

### Check Draft

```
/commscribe check [paste draft]
```

1. Runs validation for current tier
2. Checks AI pattern density
3. Evaluates voice match (if profile exists)
4. Returns actionable feedback
