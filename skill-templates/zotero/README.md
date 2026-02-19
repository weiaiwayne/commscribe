# Zotero Integration for CommScribe

Connect your Zotero library for:
1. **Voice Learning** — Extract writing samples from YOUR published papers
2. **Literature Search** — Find relevant citations in your existing library
3. **Citation Management** — Proper formatting and verification

## Quick Start

### 1. Get Your Zotero Credentials

1. Go to [zotero.org/settings/keys](https://www.zotero.org/settings/keys)
2. Create a new API key with **read access**
3. Note your **User ID** (shown on the same page)

### 2. Configure CommScribe

**Option A: Environment Variables**
```bash
export ZOTERO_USER_ID="your_user_id"
export ZOTERO_API_KEY="your_api_key"
```

**Option B: Config File**
```bash
# Create config
cat > ~/.commscribe/zotero.json << EOF
{
  "user_id": "your_user_id",
  "api_key": "your_api_key"
}
EOF
```

**Option C: Pass at Runtime**
```bash
python zotero_client.py --user-id YOUR_ID --api-key YOUR_KEY
```

### 3. Test Connection

```bash
python zotero_client.py --test
```

## Features

### Voice Sample Extraction

Pull your solo-authored papers for voice learning:

```python
from zotero_client import ZoteroClient

client = ZoteroClient()

# Get papers where you're the only author
my_papers = client.get_solo_authored(limit=10)

# Extract text for voice learning
samples = [client.get_full_text(paper) for paper in my_papers]
```

### Literature Search

Search your existing library:

```python
# Search by keyword
results = client.search("networked gatekeeping")

# Search by collection
results = client.get_collection("Gatekeeping Theory")

# Get papers citing a specific work
results = client.citing("Meraz & Papacharissi 2013")
```

### Citation Formatting

```python
# Get formatted citation
cite = client.format_citation(item_key, style="apa")
# → "Meraz, S., & Papacharissi, Z. (2013). Networked gatekeeping..."

# Get BibTeX
bibtex = client.get_bibtex(item_key)
```

## Privacy

The Zotero integration:
- **Only reads** your library (no write access needed)
- **Processes locally** — nothing uploaded elsewhere
- **Does not store credentials** in code (use env vars or config)
- Works with **private libraries**

## Files

| File | Description |
|------|-------------|
| `zotero_client.py` | Main Zotero API client |
| `voice_extractor.py` | Extract writing samples for voice learning |
| `citation_search.py` | Search and format citations |

## Troubleshooting

**"pyzotero not installed"**
```bash
pip install pyzotero
```

**"Unauthorized"**
- Check API key has read access
- Verify user ID is numeric (not username)

**"No full text"**
- Zotero doesn't store full text via API
- Use PDF paths if stored locally, or retrieve via DOI

---

*Part of CommScribe — Literature Review & Theorization Framework*
