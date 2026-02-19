---
name: literature-synthesis
description: Stage 2 - Search and synthesize literature
triggers:
  - synthesize literature
  - search papers
  - find literature
  - literature review search
---

# Stage 2: Literature Synthesis

## Purpose

Search, retrieve, and synthesize relevant literature based on your validated concept plan.

---

## Search Methods

CommScribe uses three complementary search approaches:

### 1. Two-Stage Retrieval (~0.2s)

**Stage 1:** Fast keyword filtering (Jaccard similarity)
**Stage 2:** Semantic reranking with embeddings

```python
# From your Zotero library
results = search_zotero_two_stage(
    query="networked gatekeeping algorithmic curation",
    top_k=20,
    candidate_pool=100
)
```

**Best for:** Quick exploration, known-item search

### 2. Three-Path Retrieval (~0.4s)

**Path 1:** Keyword/Jaccard (30% weight)
**Path 2:** Embedding similarity (60% weight)
**Path 3:** Domain matching (10% weight)

```python
results = search_zotero_three_path(
    query="how do algorithms change gatekeeping power",
    top_k=20
)
```

**Best for:** Conceptual queries, finding related work

### 3. Hybrid Search (~1.5s)

**Sources:**
- Zotero Knowledge Graph (your library)
- OpenAlex API (80M+ papers)
- Semantic Scholar API (optional)

**Deduplication:** By DOI, title similarity

```python
results = search_hybrid(
    query="networked gatekeeping",
    zotero_weight=0.6,
    openalex_weight=0.4,
    top_k=30
)
```

**Best for:** Comprehensive search, finding papers outside your library

---

## Search Strategy

### From Concept to Queries

Your concept plan generates search queries:

| Concept Element | Generated Query |
|-----------------|-----------------|
| Research question | "algorithmic curation gatekeeping power" |
| Theory | "Meraz Papacharissi networked gatekeeping" |
| Key authors | "author:Gillespie platform governance" |
| Scope | "Twitter Facebook algorithmic feed 2016-2025" |

### Query Expansion

System suggests related queries:

```
Primary query: "networked gatekeeping"

Suggested expansions:
→ "algorithmic gatekeeping" (related concept)
→ "platform governance" (broader)
→ "news curation social media" (applied context)
→ "Meraz Papacharissi 2013" (foundational)

Include expansions? (yes/select/no)
```

---

## Synthesis Workflow

### Step 1: Initial Search

```
/commscribe synthesize literature

System: "Searching based on your concept plan...

Queries:
1. 'networked gatekeeping algorithmic' → 18 results
2. 'platform governance curation' → 23 results
3. 'Meraz Papacharissi gatekeeping' → 7 results

Total unique papers: 41
From your Zotero: 28
New from OpenAlex: 13

Review results? (yes/filter/proceed)"
```

### Step 2: Relevance Filtering

```
Highly relevant (score > 0.8): 12 papers
Moderately relevant (0.5-0.8): 19 papers
Marginally relevant (< 0.5): 10 papers

Show: [highly relevant] [all] [let me filter manually]
```

### Step 3: Organize by Theme

System suggests thematic organization:

```
Suggested themes (from your concept):

1. Classic gatekeeping theory
   → White 1950, Shoemaker & Vos 2009 (4 papers)

2. Networked gatekeeping
   → Meraz & Papacharissi 2013, Barzilai-Nahon 2008 (8 papers)

3. Algorithmic curation
   → Gillespie 2018, Bucher 2018 (11 papers)

4. Hybrid media systems
   → Chadwick 2017 (6 papers)

5. Empirical studies
   → Platform-specific research (12 papers)

Accept organization? (yes/modify)
```

### Step 4: Generate Synthesis Notes

For each theme, generate structured notes:

```markdown
## Theme 2: Networked Gatekeeping

### Key Arguments

**Meraz & Papacharissi (2013):**
- Gatekeeping power distributed across network
- Multiple gatekeeper types: traditional media, influential bloggers, active users
- Power measured by network centrality, not institutional position

**Barzilai-Nahon (2008):**
- Network gatekeeping theory
- Gatekeeping as process, not role
- Four mechanisms: selection, addition, withholding, channeling

### Tensions/Debates

- Does networked = democratized? (Meraz: partially; critics: power still concentrates)
- Measurement challenges: How to identify gatekeepers empirically?

### Gaps

- Framework predates algorithmic feeds (pre-2013)
- Doesn't account for platform-level curation
- Assumes human agency in gatekeeping decisions

### Connection to Your Argument

This framework provides foundation but needs extension for algorithmic context.
Your contribution: Adding algorithmic gatekeepers to the typology.
```

---

## Citation Management

### [VERIFY] Tags

When uncertain about a citation:

```markdown
Meraz and Papacharissi (2013) argue that gatekeeping power has shifted 
from institutional positions to network centrality [VERIFY: exact quote on p. 12?].
```

**Draft tier:** [VERIFY] tags allowed
**Publication tier:** All must be resolved

### Citation Density

Track citation density to match your voice profile:

```
Your profile: 2.3 citations per 100 words
Current synthesis: 3.1 citations per 100 words

Note: Synthesis notes typically have higher citation density.
Will adjust during drafting stage.
```

---

## Output

Stage 2 produces:

```
project/
├── CONCEPT.md           # From Stage 1
├── LITERATURE.md        # Synthesized notes
├── sources/
│   ├── search_results.json
│   ├── theme_1_classic.md
│   ├── theme_2_networked.md
│   ├── theme_3_algorithmic.md
│   └── theme_4_empirical.md
└── bibliography.bib     # Collected references
```

### LITERATURE.md Structure

```markdown
# Literature Synthesis: [Topic]

## Overview
- Papers reviewed: 41
- Themes identified: 4
- Key debates: 3
- Gaps found: 2

## Theme 1: Classic Gatekeeping
[synthesis notes]

## Theme 2: Networked Gatekeeping
[synthesis notes]

## Theme 3: Algorithmic Curation
[synthesis notes]

## Theme 4: Empirical Studies
[synthesis notes]

## Cross-Cutting Debates
[tensions across themes]

## Identified Gaps
[what's missing that your review addresses]

## Recommended Structure for Draft
[suggested outline based on synthesis]
```

---

## Proceeding to Stage 2.5/3

After synthesis:

```
✅ SYNTHESIS COMPLETE

Papers reviewed: 41
Themes organized: 4
Notes generated: 4,200 words
Gaps identified: 2

Before drafting, would you like to:
[ ] Setup voice profile (Stage 2.5) — RECOMMENDED if first time
[ ] Proceed to drafting (Stage 3) — Uses existing profile or default

Your choice: ___
```

---

*Good synthesis makes drafting easy. Bad synthesis makes drafting painful.*
