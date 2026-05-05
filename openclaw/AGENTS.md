# CommScribe OpenClaw Integration

## Hybrid Model Routing (NEW v0.3.0)

CommScribe now uses **dynamic model selection** based on content complexity, urgency, and task requirements. The `HybridModelRouter` intelligently selects the optimal model for each task.

### How It Works

```python
from commscribe.scripts.model_router import (
    HybridModelRouter, TaskType, UrgencyLevel, create_router
)

# Create router instance
router = create_router(prefer_reasoning=True)

# Route a task
decision = router.route(
    task_type=TaskType.DRAFTING,
    content=concept_text,
    urgency=UrgencyLevel.QUALITY  # FAST | BALANCED | QUALITY
)

# Get OpenClaw configuration
config = router.get_recommended_config(decision)
print(f"Selected: {decision.selected_model}")
print(f"Reasoning: {decision.reasoning}")
print(f"Confidence: {decision.confidence:.2f}")
```

### Routing Decision Output

```python
RoutingDecision(
    task_type=TaskType.DRAFTING,
    selected_model="anthropic/claude-opus-4.5",  # Dynamically chosen
    complexity_tier=ComplexityTier.HIGH,           # Based on content analysis
    urgency=UrgencyLevel.QUALITY,
    confidence=0.92,
    reasoning="Selected anthropic/claude-opus-4.5 for drafting with quality priority; Content complexity: high; Prioritized quality (score: 0.96); Alternative: openai/gpt-4o",
    alternatives=["openai/gpt-4o", "anthropic/claude-opus-4"],
    estimated_cost=0.45,
    estimated_time_seconds=600
)
```

### Complexity Analysis

The router automatically analyzes content complexity based on:

| Factor | Indicators |
|--------|-----------|
| **Length** | Word count thresholds (1K/5K/10K+) |
| **Vocabulary** | Academic terminology density |
| **Citations** | Citation count and density |
| **Nuance** | Markers: however, tension, paradoxically |
| **Domain** | Task-specific terminology |

Results in tiers: `LOW` | `MEDIUM` | `HIGH` | `EXTREME`

### Model Registry

| Model | Speed | Quality | Cost/1K | Best For |
|-------|-------|---------|---------|----------|
| `google/gemini-2.0-flash` | 0.95 | 0.75 | $0.00015 | Fast synthesis, retrieval |
| `openai/gpt-4o-mini` | 0.90 | 0.70 | $0.00015 | Quick analysis |
| `anthropic/claude-3.5-sonnet` | 0.75 | 0.85 | $0.003 | Balanced, voice matching |
| `openai/gpt-4o` | 0.70 | 0.88 | $0.0025 | Audit, critical review |
| `openai/o3-mini` | 0.60 | 0.92 | $0.008 | Reasoning, structured analysis |
| `anthropic/claude-opus-4` | 0.55 | 0.95 | $0.015 | Quality drafting |
| `anthropic/claude-opus-4.5` | 0.52 | 0.96 | $0.018 | Best creative writing |

---

## Multi-Agent Workflow (with Hybrid Routing)

### Recommended Approach

Replace static model assignments with dynamic routing:

```python
# OLD: Static assignment
model = "anthropic/claude-opus-4.5"  # Always

# NEW: Dynamic routing
router = create_router(prefer_reasoning=True)
decision = router.get_model_for_stage(stage="drafting", content=draft_text)
model = decision.selected_model  # Chosen based on content
```

### Stage-Based Routing

```python
from commscribe.scripts.model_router import HybridModelRouter, UrgencyLevel

router = HybridModelRouter()

# Stage 1: Concept Validation
if detection["stage"] == "concept_plan":
    decision = router.get_model_for_stage(
        "concept_validation", 
        content=concept_text,
        urgency=UrgencyLevel.FAST  # Quick validation
    )

# Stage 2: Literature Synthesis
decision = router.get_model_for_stage(
    "synthesis",
    content=research_question,
    urgency=UrgencyLevel.FAST  # Prefer speed for search
)

# Stage 3: Drafting (complexity-aware)
decision = router.get_model_for_stage(
    "drafting",
    content=synthesis_notes,  # Analyzed for complexity
    urgency=UrgencyLevel.QUALITY  # Always quality for drafting
)

# Stage 4: Audit
decision = router.get_model_for_stage(
    "audit",
    content=draft_text,
    urgency=UrgencyLevel.BALANCED
)
```

### Using sessions_spawn with Hybrid Router

```yaml
# The router generates optimal configs for OpenClaw

# Example: Dynamically routed synthesis
sessions_spawn:
  task: |
    {{SYNTHESIS_TASK}}
  model: "{{ROUTER_SELECTED_MODEL}}"
  runTimeoutSeconds: {{ROUTER_ESTIMATED_TIME}}
  
# Behind the scenes:
# - Analyzes content complexity
# - Selects model based on urgency + complexity
# - Sets appropriate timeout
```

Full Python integration:

```python
from commscribe.scripts.model_router import create_router, TaskType, UrgencyLevel
from openclaw import sessions_spawn

router = create_router()

# Analyze and route
content = "Research on algorithmic curation and climate discourse..."
decision = router.route(
    TaskType.SYNTHESIS,
    content,
    UrgencyLevel.FAST
)

config = router.get_recommended_config(decision)

# Spawn with dynamically selected model
sessions_spawn(
    task=f"Synthesize literature on: {topic}",
    model=config["model"],
    runTimeoutSeconds=config["runTimeoutSeconds"],
    metadata={
        "routing": config["routing"],
        "hybrid_routed": True
    }
)
```

### Decision Logging

All routing decisions are logged for future analysis:

```python
# View recent decisions
for entry in router.routing_history[-5:]:
    print(f"{entry['timestamp']}: {entry['decision']['selected_model']}")
    print(f"  Confidence: {entry['decision']['confidence']}")
    print(f"  Reasoning: {entry['decision']['reasoning']}")
```

---

## Legacy Support

For backwards compatibility, static assignments are still available:

```python
from commscribe.scripts.model_router import LEGACY_MODEL_ASSIGNMENTS

# Get legacy model for task type
model = LEGACY_MODEL_ASSIGNMENTS[TaskType.SYNTHESIS]
# "google/gemini-2.0-flash"
```

---

## Multi-Agent Workflow (Legacy - Static Assignments)

> **Note**: The following section documents static assignments for reference. 
> New implementations should use Hybrid Routing (above).

### Static Model Assignments

| Stage | Task | Model | Why |
|-------|------|-------|-----|
| **Synthesis** | Literature search | `google/gemini-2.0-flash` | Fast, good at retrieval |
| **Drafting** | Voice-constrained writing | `anthropic/claude-opus-4-5` | Best creative writing |
| **Audit** | Critical review | `openai/gpt-4o` | Different perspective |
| **Voice Setup** | Extract profile | `anthropic/claude-sonnet-4-5` | Good balance |

### Using sessions_spawn (Static)

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

---

## Cron Jobs for Long-Running Tasks

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

---

## Session Workflow Example

Full literature review as a session:

```python
from commscribe.scripts.model_router import create_router, TaskType, UrgencyLevel
from commscribe.scripts.validation import validate_concept

router = create_router(prefer_reasoning=True)

# 1. Validate concept
validation = validate_concept(concept_text)
if not validation.passed:
    return f"Concept needs revision: {validation.issues}"

# 2. Spawn synthesis agent (dynamic routing)
decision = router.route(TaskType.SYNTHESIS, research_question, UrgencyLevel.FAST)
config = router.get_recommended_config(decision)

sessions_spawn(
    task=f"Synthesize literature on: {research_question}",
    model=config["model"],
    runTimeoutSeconds=config["runTimeoutSeconds"],
    label="synthesis-agent"
)

# 3. When synthesis complete, spawn drafting agent (complexity-aware)
decision = router.route(TaskType.DRAFTING, synthesis_result, UrgencyLevel.QUALITY)
config = router.get_recommended_config(decision)

sessions_spawn(
    task=f"Draft introduction using synthesis notes and voice profile",
    model=config["model"],
    runTimeoutSeconds=config["runTimeoutSeconds"],
    label="drafting-agent"
)

# 4. When draft complete, spawn audit agent
decision = router.route(TaskType.AUDIT, draft_text, UrgencyLevel.BALANCED)
config = router.get_recommended_config(decision)

sessions_spawn(
    task=f"Audit this draft: {draft_text}",
    model=config["model"],
    runTimeoutSeconds=config["runTimeoutSeconds"],
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
from commscribe.scripts.validation import validate_concept, validate_draft
from commscribe.scripts.model_router import create_router, TaskType, UrgencyLevel

router = create_router()

# After concept submission
concept_result = validate_concept(concept_text)
if not concept_result.passed:
    message(f"❌ Concept needs work:\n{concept_result}")
    return

# Select appropriate validation model (complexity-aware)
decision = router.route(TaskType.VALIDATION, draft_text, UrgencyLevel.FAST)
print(f"Using {decision.selected_model} for validation")

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
3. **Routes** to optimal synthesis model based on complexity
4. Spawns synthesis agent
5. Notifies when synthesis ready
6. Asks if ready to draft
7. **Routes** to optimal drafting model (always quality)
8. Spawns drafting agent with voice profile
9. Returns draft with audit comments

### Setup Voice Profile

```
/commscribe setup voice
```

1. Asks for 5-10 writing samples
2. Offers: paste text / file paths / Zotero pull
3. **Routes** to voice extraction model
4. Extracts statistical + adaptive profile
5. Asks if wants contrast samples (AI text)
6. Saves profile for future use

### Check Draft

```
/commscribe check [paste draft]
```

1. **Routes** to validation model based on complexity
2. Runs validation for current tier
3. Checks AI pattern density
4. Evaluates voice match (if profile exists)
5. Returns actionable feedback

---

## Migration Guide: Static → Hybrid Routing

### Before (Static)

```python
# Always use same models
SYNTHESIS_MODEL = "google/gemini-2.0-flash"
DRAFTING_MODEL = "anthropic/claude-opus-4.5"
AUDIT_MODEL = "openai/gpt-4o"

sessions_spawn(task=task1, model=SYNTHESIS_MODEL, timeout=300)
sessions_spawn(task=task2, model=DRAFTING_MODEL, timeout=600)
```

### After (Hybrid)

```python
from commscribe.scripts.model_router import create_router, TaskType, UrgencyLevel

router = create_router()

# Dynamically select based on content + requirements
for task, task_type in [(task1, TaskType.SYNTHESIS), 
                        (task2, TaskType.DRAFTING)]:
    decision = router.route(task_type, task.content, UrgencyLevel.QUALITY)
    config = router.get_recommended_config(decision)
    
    sessions_spawn(
        task=task.content,
        model=config["model"],
        runTimeoutSeconds=config["runTimeoutSeconds"]
    )
```

### Key Benefits

1. **Cost optimization**: Fast task? Use cheaper model. Complex task? Use better model.
2. **Auto-scaling**: Short content uses faster models, long content uses models with larger context
3. **Smart fallbacks**: Alternatives provided if primary model unavailable
4. **Transparency**: Every routing decision includes reasoning and confidence score