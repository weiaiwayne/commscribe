---
name: commscribe
description: Unblock your scholarship — helps with writer's block while keeping your voice central
metadata:
  version: 0.1.0
  author: Wayne Xu / LampBotics AI Lab
  sister_project: commDAAF
---

# CommScribe — Unblock Your Scholarship

**Version 0.1.0**

*Your ideas. Your voice. We just help you get unstuck.*

**The problem:** Writer's block, literature overwhelm, revision paralysis — the friction that stops scholars from doing their best work.

**What we DON'T do:**
- ❌ Write your paper for you
- ❌ Generate arguments (that's YOUR job)
- ❌ Replace reading the literature
- ❌ Make bad ideas sound good
- ❌ Work without your input

**What we DO:**
- Helps you push through mental blocks
- Handles tedious busywork (lit search, organization)
- Keeps YOUR voice at the center, always
- Learns YOUR style, not generic academic-ese

---

## Trigger Patterns

Activate this skill when user requests involve:
- "literature review on [topic]"
- "write about [theory/concept]"
- "synthesize research on [topic]"
- "theorize [phenomenon]"
- "draft a section on [topic]"
- "review my draft"
- "setup voice profile"
- "write in my voice"

---

## Agent Notes: Transparent Thinking

Throughout all outputs, agents insert honest notes about their reasoning, uncertainty, and suggestions:

```markdown
## Literature Review

The networked public sphere has transformed how information flows 
through society (Benkler, 2006) [Z].

📝 *Agent note: I'm connecting this to your RQ about platform governance, 
but you might frame it differently — this is one possible thread.*

Recent work suggests algorithmic curation acts as a form of gatekeeping 
(Thorson & Wells, 2016) [?].

⚠️ *Agent note: I'm less familiar with the 2020s literature here. 
There's probably newer work you should check.*

The relationship between legacy media and social platforms remains 
contested, with some arguing for...

🤔 *Agent note: I'm hedging here because the literature genuinely 
disagrees. You'll need to take a position.*
```

### Agent Note Types

| Emoji | Type | When to Use |
|-------|------|-------------|
| 📝 | **Reasoning** | Explaining why I made a choice |
| ⚠️ | **Uncertainty** | I'm not confident about this |
| 🤔 | **Decision point** | You need to make a call here |
| 💡 | **Suggestion** | Optional improvement idea |
| 📚 | **Citation note** | Verify this reference |
| ✂️ | **Cuts available** | This could be shortened |
| 🔗 | **Connection** | Links to another section/paper |

### Why Agent Notes?

1. **Transparency** — You see our reasoning, not just output
2. **Calibration** — We flag our own uncertainty
3. **Collaboration** — Feels like a coauthor, not a black box
4. **Learning** — You can correct us and we improve

### Stripping Notes for Final

Before submission, run:
```
/commscribe strip-notes

→ Removes all agent notes
→ Flags any unresolved [VERIFY] or [??] tags
→ Produces clean output
```

---

## The 4-Stage Workflow

| Stage | You Have | You Want | Entry |
|-------|----------|----------|-------|
| **1️⃣ Concept** | Research idea | Validated concept plan | "start lit review on..." |
| **2️⃣ Synthesis** | Validated concept | Literature integration | "synthesize literature on..." |
| **3️⃣ Drafting** | Literature notes | Written draft | "draft section on..." |
| **4️⃣ Audit** | Complete draft | Critical review | "audit my draft" |

### Stage 1: Concept Planning (GATED)

**Validation Requirements:**
- Minimum 300 words
- At least 3 citations
- Clear research question
- Theoretical framing
- Original voice (not generic AI)

**If validation fails:** Return specific feedback, require revision.

### Stage 2: Literature Synthesis

**Default: Zotero-first search**
Start with user's existing library. Often sufficient.

**Expanded search (optional):**
```
📚 Agent nudge: Your Zotero has 12 papers on this topic. 
Want me to expand the search?

Options:
1. No, use my library only (faster, papers I trust)
2. Yes, search OpenAlex for recent work (adds ~50 candidates)
3. Yes, full semantic search (slower, most comprehensive)

Your choice? ___
```

| Mode | Sources | Speed | When to Use |
|------|---------|-------|-------------|
| **Library only** | Zotero | Fast | You know the lit well |
| **+ OpenAlex** | Zotero + OpenAlex API | Medium | Need recent papers |
| **+ Semantic** | Above + embedding search | Slow | New area, comprehensive review |

**Output:** Integrated literature notes with citations.

### Stage 2.5: Voice Learning (Optional but Recommended)

**Two modes available:**

#### Statistical Mode (Traditional)
- Sentence length patterns
- Vocabulary richness (TTR)
- Hedging preferences
- Transition usage
- Citation integration style

#### Adaptive Mode (AI-Native) ⭐ NEW
- **Embedding-based** — captures holistic feel, not just word counts
- **Continuous learning** — improves with each feedback
- **Contrastive** — learns what your voice is NOT (vs AI, vs generic academic)
- **Feedback-driven** — "sounds like me" / "doesn't" calibrates the model

```python
# Adaptive voice learns and improves
manager.setup_voice("wayne", samples, 
    contrast_samples={"ai_generated": ai_texts})

# Later: feedback refines it
manager.feedback("wayne", generated_text, sounds_like_me=True)
```

**Sample Requirements:**
- 5-10 samples
- 500+ words each
- User's own writing (solo-authored preferred)

**Accepted formats:**
| Format | Support | Notes |
|--------|---------|-------|
| `.txt` | ✅ | Plain text, cleanest |
| `.md` | ✅ | Markdown preserved |
| `.docx` | ✅ | Word 2007+, extracts text + comments |
| `.doc` | ⚠️ | Legacy Word, best-effort |
| `.pdf` | ✅ | Extracts text (not scanned images) |
| `.rtf` | ✅ | Rich text, strips formatting |

**Word comments & track changes supported!**

If you add comments in Word (Review → New Comment), the agent reads them:

```markdown
## 💬 USER COMMENTS FROM DOCUMENT

**[Comment by Wayne]:** This transition feels weak, help me fix it
  ↳ *On text:* "Furthermore, the implications..."
```

If you have Track Changes enabled, the agent sees those too:

```markdown
## 📝 TRACK CHANGES IN DOCUMENT

**[+Wayne]:** ++networked gatekeeping theory++
**[-Wayne]:** ~~traditional gatekeeping~~
```

### Agent Output with Track Changes

When the agent edits, it shows changes in a similar format:

```markdown
~~Furthermore, the implications are significant.~~
→ ++This reframing of gatekeeping as a networked process shifts our understanding...++
```

**To get a proper .docx with Track Changes:**
```
/download --track-changes
```

This generates a Word file where edits appear as tracked changes you can accept/reject in Word.

📝 *Agent note: Track changes export uses python-redlines. 
If not installed, you'll get a clean doc with changes already applied.*

```
📝 Agent nudge: Drop your files or paste text directly.
I accept .docx, .pdf, .txt, and more.

If pasting, just paste the text — no need to format it.
```

**Custom instructions with uploads:**

Users can add notes when uploading samples:

```
📎 paper_intro.docx
💬 "This is my strongest writing — weight this heavily"

📎 methods_draft.pdf  
💬 "Ignore this section's passive voice, it was required by the journal"

📎 dissertation_ch3.docx
💬 "Focus on theoretical arguments, skip the lit review parts"
```

**Instruction types:**
| Instruction | Effect |
|-------------|--------|
| "Weight heavily" | Higher influence on voice profile |
| "Ignore X" | Exclude specific patterns |
| "Focus on Y" | Prioritize certain sections/styles |
| "This is [section type]" | Context for style extraction |
| "I want to change X" | Learn voice but not this habit |

```
📝 Agent nudge: Any notes about these samples?

Examples:
- "The first one is my best writing"
- "Ignore the passive voice in paper2, it was journal-required"
- "I want to be less hedge-y than these samples show"

Or just press Enter to continue without notes.
```

### Stage 3: Drafting (Voice-Constrained)

**Generation with voice profile:**
- Match sentence patterns
- Use preferred hedges/transitions
- Maintain vocabulary richness
- Avoid AI patterns (286 banned phrases)

**Multi-draft support:**
- Unlimited iterations (practical limit ~10 before context overflow)
- Agent comments on each version
- Full version history preserved

---

## Iterative Revision Workflow

Writing is a conversation. Upload once, then talk.

### The Flow

```
1. User uploads draft.docx
2. Agent responds with edits + questions
3. User replies in chat: "Option A. Cut that paragraph."
4. Agent applies changes, shows result, asks next questions
5. User replies: "Looks good. Now fix the methods section."
6. Agent continues...
7. When done: User downloads final version
```

### Example Conversation

**User:** [uploads draft.docx]  
*"Help me strengthen the theoretical framing."*

**Agent:**
> Here's your draft with my suggested edits:
> 
> ~~Furthermore, the implications are significant.~~  
> → **This reframing of gatekeeping as networked process shifts our understanding of...**
> 
> 📝 I restructured paragraphs 2-3 to connect Barzilai-Nahon to your RQ.
> 
> 🤔 Question: On p.4 you mention "platform affordances" — do you mean technical features or social norms? I need to know before editing that section.
> 
> 💬 Also: Option A (keep Castells) or Option B (cut him)?

**User:** *"Technical features. Option B, cut Castells. Also make methods less passive."*

**Agent:**
> ✅ Clarified affordances = technical features  
> ✅ Removed Castells reference  
> ✅ Revised methods to active voice:
> 
> ~~Data were collected from~~ → **We collected data from**  
> ~~Analysis was conducted~~ → **We analyzed**
> 
> 📝 Is that too informal for your target journal?
> 
> Here's the updated draft: [shows full text]

**User:** *"Perfect. What about the conclusion?"*

**Agent:** *[continues...]*

### No Need to Re-upload

The agent maintains the working document in memory. Just talk:
- "Fix paragraph 3"
- "Make that shorter"  
- "I don't like that phrasing"
- "Add a transition here"
- "What about the lit review?"

Re-upload only if you edited offline and want to sync.

### Commands

| Command | Action |
|---------|--------|
| `/show` | Display current draft |
| `/download` | Get current version as file |
| `/diff` | Show all changes since upload |
| `/undo` | Revert last change |
| `/history` | Show revision log |

### Agent Behavior

**Always:**
- Show what changed (strikethrough → new)
- Explain reasoning for edits
- Ask before guessing
- Offer options when multiple approaches exist

**Never:**
- Make silent changes
- Override explicit preferences
- Require file uploads for every change

---

## Learning From Feedback

The agent learns from every interaction and gets better at matching your preferences.

### What Gets Learned

| Feedback Type | Example | What Agent Learns |
|---------------|---------|-------------------|
| **Accept edit** | User keeps agent's change | "This edit style works" |
| **Reject edit** | User reverts or rewrites | "Don't do this again" |
| **Explicit praise** | "Perfect!" | Reinforce that approach |
| **Explicit correction** | "Too formal" | Adjust tone preference |
| **Repeated requests** | "Make it shorter" (3x) | Default to concise |

### Learning Storage

```
project/
├── VOICE_PROFILE.json      # Writing style
├── PREFERENCES.json        # Learned preferences
│   ├── edits_accepted: [...]
│   ├── edits_rejected: [...]
│   ├── tone_adjustments: {...}
│   ├── common_requests: [...]
│   └── explicit_rules: [...]
└── REVISION_HISTORY.json   # Full interaction log
```

### Example Learning Cycle

**Session 1:**
```
Agent: "Changed 'important' → 'significant'"
User: "No, keep 'important'. I don't like thesaurus swaps."
→ Agent saves: { "avoid": "synonym_substitution" }
```

**Session 2:**
```
Agent: [Doesn't suggest synonym swaps anymore]

📝 Agent note: I'm not suggesting word swaps because 
you told me you don't like them. Say "/preferences reset" 
to clear learned preferences.
```

### Explicit Rules

Users can also set explicit preferences:

```
User: "Never use 'Furthermore' or 'Moreover'"
→ Agent saves: { "banned_words": ["Furthermore", "Moreover"] }

User: "Always use Oxford comma"
→ Agent saves: { "oxford_comma": true }

User: "I prefer active voice"
→ Agent saves: { "voice_preference": "active" }
```

### Commands

| Command | Action |
|---------|--------|
| `/preferences` | Show learned preferences |
| `/preferences reset` | Clear all learned preferences |
| `/preferences add [rule]` | Add explicit rule |
| `/preferences remove [rule]` | Remove a rule |

### Cross-Session Learning

Preferences persist across sessions. When you start a new project:

```
📝 Agent note: Loading your preferences from previous sessions:
- Avoid synonym substitution
- Prefer active voice  
- Use Oxford comma
- 23 edits accepted, 5 rejected (82% approval rate)

Type /preferences to review or /preferences reset to start fresh.
```

### Privacy Note

All learning is local to your workspace. Nothing leaves your machine unless you explicitly export it.

### Stage 4: Independent Audit

**Different model reviews:**
- Logical coherence
- Argument strength
- Citation accuracy
- AI pattern check
- Voice consistency

---

## Engagement Modes

### Concept Mode
**Triggers:** "start", "begin", "new literature review"

Validate research concept before proceeding.

### Synthesis Mode
**Triggers:** "synthesize", "search literature", "find papers"

Search and integrate literature.

### Drafting Mode
**Triggers:** "write", "draft", "compose"

Generate text in user's voice.

### Audit Mode
**Triggers:** "review", "audit", "critique my draft"

Critical review with actionable feedback.

### Voice Setup Mode
**Triggers:** "setup voice", "learn my style", "extract voice"

Create voice profile from samples.

---

## Anti-AI Pattern Enforcement

**286 patterns across 10 categories:**

1. **Generic Openers** — "In recent years", "With the rise of"
2. **Importance Phrases** — "It is important to note"
3. **Overused Transitions** — "Furthermore", "Moreover"
4. **Excessive Hedging** — "could potentially possibly"
5. **Filler Phrases** — "a wide range of"
6. **Structural Patterns** — "Let's dive in"
7. **Inflated Adjectives** — "groundbreaking", "transformative"
8. **Emoji/Symbols** — 🔑💡✨ in academic text
9. **Academic AI Patterns** — "This paper aims to fill a gap"
10. **Conclusion Clichés** — "In conclusion", "All in all"

**Enforcement:** Prompt-based instruction before generation.

---

## Tiered Validation

| Tier | Time | Use Case | Requirements |
|------|------|----------|--------------|
| 🟢 **Notes** | 30 min | Brainstorming | Minimal—exploration allowed |
| 🟡 **Draft** | 2-4 hrs | Advisor review | Citations required, [VERIFY] tags OK |
| 🔴 **Publication** | 1-2 days | Journal submission | Full verification, no [VERIFY] tags |

---

## Agent Invocation

```yaml
# Literature search (fast model)
sessions_spawn:
  task: "Search literature on {topic}"
  model: google/gemini-2.0-flash

# Synthesis (reasoning model)
sessions_spawn:
  task: "Synthesize {papers} into integrated review"
  model: anthropic/claude-sonnet-4-5

# Drafting (quality model)
sessions_spawn:
  task: "Draft section with voice profile: {profile}"
  model: anthropic/claude-opus-4-5

# Audit (DIFFERENT model than drafting)
sessions_spawn:
  task: "Critically audit this draft: {draft}"
  model: openai/gpt-4o
```

---

## Available Skills

### Stages
- `stages/concept.md` — Concept validation workflow
- `stages/synthesis.md` — Literature search & integration
- `stages/drafting.md` — Voice-constrained generation
- `stages/audit.md` — Independent critical review

### Voice Learning
- `voice/extraction.md` — Extract style from samples (statistical)
- `voice/prompting.md` — Voice-constrained prompts
- `voice/adaptive.md` — AI-native voice learning with feedback ⭐ NEW
- `voice/profiles/` — Stored user profiles

### Anti-AI
- `anti-ai/patterns.md` — 286 patterns to avoid
- `anti-ai/validation.md` — Pattern density checking

### Workflows
- `workflows/tiered-validation.md` — Match rigor to stakes
- `workflows/nudge-system.md` — Force conscious choices
- `workflows/reflection-checkpoints.md` — Metacognition pauses

---

## Citation Integrity

### The Honesty Principle

**AI agents hallucinate citations.** We don't pretend otherwise.

Every citation in CommScribe output comes with an honesty nudge:

```markdown
Smith (2020) argues that gatekeeping has evolved in digital spaces.

📚 *Agent note: I believe this is from "Networked Gatekeeping" — 
but I could be wrong. Please verify before citing.*
```

### Citation Confidence Levels

| Level | Marker | Meaning |
|-------|--------|---------|
| ✅ **Zotero-verified** | [Z] | Exists in your Zotero library |
| 🟡 **Likely correct** | [?] | Common citation, probably real |
| 🔴 **Uncertain** | [??] | Check this one carefully |
| ⚠️ **Reconstructed** | [R] | I know the idea exists but may have wrong author/year |

### Example Output

```markdown
## Theoretical Framework

Gatekeeping theory has evolved from Lewin's (1947) original formulation 
[Z: in your library] to networked gatekeeping (Barzilai-Nahon, 2008) 
[?? Agent note: I'm fairly confident this is the right cite, but 
please double-check the year — it might be 2009].

The concept of "network gatekeeping salience" [R: I know this concept 
exists in the literature but I'm reconstructing the citation — you'll 
need to find the actual source] suggests that...
```

### Zotero Integration

If connected to user's Zotero:
1. Check if cited work exists in library
2. Mark with [Z] if verified
3. Suggest similar papers from library if uncertain
4. Flag citations that don't match any library item

### [VERIFY] Tag System

For structural uncertainties (not just citation accuracy):
```
Smith (2020) argues that gatekeeping has evolved [VERIFY: exact page number needed]
```

**Draft tier:** [VERIFY] tags and confidence markers allowed  
**Publication tier:** All tags must be resolved, all citations verified

### Citation Density Matching

Voice profile includes citation density:
- Extract from user's samples
- Match in generated text
- Flag if significantly different

### The Bottom Line

We'd rather say "I might be wrong" than confidently cite something fake. 
Your credibility matters more than our appearance of competence.

---

## Human Checkpoints

Pause and notify at:
1. After concept validation (before synthesis)
2. After synthesis (before drafting)
3. After each draft iteration
4. Before final delivery

---

## Project Structure

```
project/
├── CONCEPT.md         # Validated concept plan
├── LITERATURE.md      # Synthesized notes
├── VOICE_PROFILE.json # User's voice profile
├── drafts/
│   ├── v1.md
│   ├── v2.md
│   └── v3.md
├── audit/
│   └── review.md
└── FINAL.md
```

---

## Quick Start

### New Literature Review

```
/commscribe start literature review on networked gatekeeping

→ System asks for concept plan
→ User provides concept (300+ words, 3+ citations)
→ System validates
→ Proceeds to synthesis
```

### Setup Voice Profile

```
/commscribe setup voice

→ System asks for 5-10 writing samples
→ User provides samples
→ System extracts profile
→ Profile saved for future use
```

### Draft with Voice

```
/commscribe draft introduction section

→ System loads voice profile
→ Generates in user's voice
→ Avoids AI patterns
→ Returns draft with comments
```

---

## Integration with CommDAAF

CommScribe handles writing; CommDAAF handles analysis.

**Shared components:**
- Tiered validation
- Nudge system
- Zotero integration
- Research integrity guardrails

**Handoff points:**
- CommDAAF results → CommScribe discussion section
- CommScribe literature → CommDAAF methodology framing

---

*Write like yourself — not like an AI pretending to be you.*
