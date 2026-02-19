#!/usr/bin/env python3
"""
Zotero Client for CommScribe

Connects to user's Zotero library for:
- Voice learning (extract writing samples from published papers)
- Literature search (find citations in existing library)
- Citation management (format and verify)

Usage:
    python zotero_client.py --test
    python zotero_client.py --search "networked gatekeeping"
    python zotero_client.py --solo-authored --limit 10

Requirements:
    pip install pyzotero requests
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass, asdict
from datetime import datetime

try:
    from pyzotero import zotero
except ImportError:
    print("Error: pyzotero not installed. Run: pip install pyzotero")
    sys.exit(1)


@dataclass
class ZoteroItem:
    """Structured Zotero item"""
    key: str
    title: str
    authors: List[str]
    year: Optional[str]
    item_type: str
    abstract: Optional[str]
    doi: Optional[str]
    url: Optional[str]
    tags: List[str]
    collections: List[str]
    
    @property
    def citation_key(self) -> str:
        """Generate citation key like 'Smith2020'"""
        first_author = self.authors[0].split()[-1] if self.authors else "Unknown"
        return f"{first_author}{self.year or 'nd'}"
    
    @property
    def apa_citation(self) -> str:
        """Generate APA-style citation"""
        if len(self.authors) == 1:
            author_str = self.authors[0]
        elif len(self.authors) == 2:
            author_str = f"{self.authors[0]} & {self.authors[1]}"
        elif len(self.authors) > 2:
            author_str = f"{self.authors[0]} et al."
        else:
            author_str = "Unknown"
        
        year = self.year or "n.d."
        return f"{author_str} ({year})"


class ZoteroClient:
    """
    Client for interacting with Zotero API.
    
    Credentials loaded from (in order):
    1. Constructor arguments
    2. Environment variables (ZOTERO_USER_ID, ZOTERO_API_KEY)
    3. Config file (~/.commscribe/zotero.json)
    """
    
    CONFIG_PATH = Path.home() / ".commscribe" / "zotero.json"
    
    def __init__(self, 
                 user_id: str = None, 
                 api_key: str = None,
                 library_type: str = "user"):
        """
        Initialize Zotero client.
        
        Args:
            user_id: Zotero user ID (numeric)
            api_key: Zotero API key with read access
            library_type: "user" or "group"
        """
        self.user_id = user_id or self._get_credential("user_id", "ZOTERO_USER_ID")
        self.api_key = api_key or self._get_credential("api_key", "ZOTERO_API_KEY")
        self.library_type = library_type
        
        if not self.user_id or not self.api_key:
            raise ValueError(
                "Zotero credentials not found. Set via:\n"
                "  1. Constructor: ZoteroClient(user_id='...', api_key='...')\n"
                "  2. Environment: ZOTERO_USER_ID, ZOTERO_API_KEY\n"
                "  3. Config file: ~/.commscribe/zotero.json"
            )
        
        self.zot = zotero.Zotero(self.user_id, library_type, self.api_key)
        self._collections_cache = None
    
    def _get_credential(self, config_key: str, env_key: str) -> Optional[str]:
        """Get credential from environment or config file"""
        # Try environment first
        value = os.environ.get(env_key)
        if value:
            return value
        
        # Try config file
        if self.CONFIG_PATH.exists():
            try:
                config = json.loads(self.CONFIG_PATH.read_text())
                return config.get(config_key)
            except:
                pass
        
        return None
    
    # -------------------------------------------------------------------------
    # CONNECTION & BASICS
    # -------------------------------------------------------------------------
    
    def test_connection(self) -> Dict[str, Any]:
        """Test API connection and return library info"""
        try:
            # Try to get key info
            key_info = self.zot.key_info()
            
            # Get item count
            items = self.zot.top(limit=1)
            total = self.zot.num_items()
            
            # Get collections
            collections = self.zot.collections()
            
            return {
                "status": "connected",
                "user_id": self.user_id,
                "total_items": total,
                "total_collections": len(collections),
                "access": key_info.get("access", {}),
            }
        except Exception as e:
            return {
                "status": "error",
                "error": str(e),
            }
    
    def get_all_items(self, limit: int = None) -> List[ZoteroItem]:
        """Get all items from library"""
        if limit:
            items = self.zot.top(limit=limit)
        else:
            items = self.zot.everything(self.zot.top())
        
        return [self._parse_item(item) for item in items]
    
    def _parse_item(self, raw: Dict) -> ZoteroItem:
        """Parse raw Zotero item into structured format"""
        data = raw.get("data", raw)
        
        # Extract authors
        authors = []
        for creator in data.get("creators", []):
            if creator.get("creatorType") == "author":
                name = f"{creator.get('firstName', '')} {creator.get('lastName', '')}".strip()
                if name:
                    authors.append(name)
        
        # Extract year from date
        date = data.get("date", "")
        year = None
        if date:
            import re
            match = re.search(r'\d{4}', date)
            if match:
                year = match.group()
        
        return ZoteroItem(
            key=data.get("key", ""),
            title=data.get("title", ""),
            authors=authors,
            year=year,
            item_type=data.get("itemType", ""),
            abstract=data.get("abstractNote"),
            doi=data.get("DOI"),
            url=data.get("url"),
            tags=[t.get("tag", "") for t in data.get("tags", [])],
            collections=data.get("collections", []),
        )
    
    # -------------------------------------------------------------------------
    # VOICE LEARNING FEATURES
    # -------------------------------------------------------------------------
    
    def get_solo_authored(self, 
                          author_name: str = None,
                          limit: int = 10) -> List[ZoteroItem]:
        """
        Get papers where user is the only author.
        Useful for voice learning (pure user voice, no collaborator influence).
        
        Args:
            author_name: Name to match (if None, returns single-author papers)
            limit: Maximum items to return
        """
        all_items = self.get_all_items()
        
        solo_papers = []
        for item in all_items:
            # Skip non-papers
            if item.item_type not in ["journalArticle", "conferencePaper", "book", "bookSection", "thesis"]:
                continue
            
            # Check if solo-authored
            if len(item.authors) == 1:
                if author_name is None or author_name.lower() in item.authors[0].lower():
                    solo_papers.append(item)
        
        return solo_papers[:limit]
    
    def get_first_authored(self, 
                           author_name: str,
                           limit: int = 20) -> List[ZoteroItem]:
        """
        Get papers where user is first author.
        Useful for voice learning (user likely wrote most of it).
        """
        all_items = self.get_all_items()
        
        first_author_papers = []
        for item in all_items:
            if item.item_type not in ["journalArticle", "conferencePaper", "book", "bookSection", "thesis"]:
                continue
            
            if item.authors and author_name.lower() in item.authors[0].lower():
                first_author_papers.append(item)
        
        return first_author_papers[:limit]
    
    def get_abstracts_for_voice(self, items: List[ZoteroItem]) -> List[str]:
        """
        Extract abstracts from items for voice learning.
        Note: Abstracts are typically 150-300 words, so need multiple.
        """
        abstracts = []
        for item in items:
            if item.abstract and len(item.abstract.split()) >= 100:
                abstracts.append(item.abstract)
        return abstracts
    
    # -------------------------------------------------------------------------
    # LITERATURE SEARCH FEATURES
    # -------------------------------------------------------------------------
    
    def search(self, query: str, limit: int = 50) -> List[ZoteroItem]:
        """
        Search library by keyword.
        Searches title, abstract, and tags.
        """
        results = self.zot.items(q=query, limit=limit)
        return [self._parse_item(item) for item in results]
    
    def get_collection(self, collection_name: str) -> List[ZoteroItem]:
        """Get all items from a named collection"""
        # Get collection ID
        if self._collections_cache is None:
            self._collections_cache = self.zot.collections()
        
        collection_id = None
        for col in self._collections_cache:
            if col["data"]["name"].lower() == collection_name.lower():
                collection_id = col["key"]
                break
        
        if not collection_id:
            raise ValueError(f"Collection '{collection_name}' not found")
        
        items = self.zot.everything(self.zot.collection_items(collection_id))
        return [self._parse_item(item) for item in items]
    
    def list_collections(self) -> List[Dict[str, Any]]:
        """List all collections"""
        collections = self.zot.collections()
        return [
            {
                "key": col["key"],
                "name": col["data"]["name"],
                "parent": col["data"].get("parentCollection"),
            }
            for col in collections
        ]
    
    def search_by_author(self, author_name: str, limit: int = 50) -> List[ZoteroItem]:
        """Search for papers by a specific author"""
        results = self.zot.items(qmode="everything", limit=limit)
        
        matching = []
        for item in results:
            parsed = self._parse_item(item)
            if any(author_name.lower() in a.lower() for a in parsed.authors):
                matching.append(parsed)
        
        return matching[:limit]
    
    def search_by_year_range(self, 
                             start_year: int, 
                             end_year: int = None) -> List[ZoteroItem]:
        """Get papers from a year range"""
        if end_year is None:
            end_year = datetime.now().year
        
        all_items = self.get_all_items()
        
        matching = []
        for item in all_items:
            if item.year:
                try:
                    year = int(item.year)
                    if start_year <= year <= end_year:
                        matching.append(item)
                except ValueError:
                    pass
        
        return sorted(matching, key=lambda x: x.year or "0000", reverse=True)
    
    # -------------------------------------------------------------------------
    # CITATION FEATURES
    # -------------------------------------------------------------------------
    
    def get_item(self, key: str) -> ZoteroItem:
        """Get a specific item by key"""
        item = self.zot.item(key)
        return self._parse_item(item)
    
    def format_citation(self, key: str, style: str = "apa") -> str:
        """
        Get formatted citation.
        Note: Uses Zotero's built-in citation formatting.
        """
        try:
            bib = self.zot.item(key, format="bib", style=style)
            return bib.strip()
        except:
            # Fallback to simple format
            item = self.get_item(key)
            return item.apa_citation
    
    def get_bibtex(self, key: str) -> str:
        """Get BibTeX entry for item"""
        return self.zot.item(key, format="bibtex")
    
    def verify_citation(self, citation_text: str) -> Optional[ZoteroItem]:
        """
        Try to match a citation to a library item.
        Useful for verifying [VERIFY] tags.
        
        Args:
            citation_text: e.g., "Meraz & Papacharissi (2013)"
        
        Returns:
            Matching ZoteroItem or None
        """
        import re
        
        # Extract author and year from citation
        match = re.search(r'([A-Z][a-z]+).*?(\d{4})', citation_text)
        if not match:
            return None
        
        author = match.group(1)
        year = match.group(2)
        
        # Search library
        all_items = self.get_all_items()
        
        for item in all_items:
            if item.year == year:
                if any(author.lower() in a.lower() for a in item.authors):
                    return item
        
        return None


# CLI
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CommScribe Zotero Client")
    parser.add_argument("--user-id", help="Zotero user ID")
    parser.add_argument("--api-key", help="Zotero API key")
    parser.add_argument("--test", action="store_true", help="Test connection")
    parser.add_argument("--search", help="Search library")
    parser.add_argument("--solo-authored", action="store_true", help="Get solo-authored papers")
    parser.add_argument("--first-authored", help="Get papers by first author name")
    parser.add_argument("--collections", action="store_true", help="List collections")
    parser.add_argument("--limit", type=int, default=10, help="Limit results")
    
    args = parser.parse_args()
    
    try:
        client = ZoteroClient(
            user_id=args.user_id,
            api_key=args.api_key
        )
    except ValueError as e:
        print(f"Error: {e}")
        sys.exit(1)
    
    if args.test:
        result = client.test_connection()
        print(json.dumps(result, indent=2))
    
    elif args.search:
        results = client.search(args.search, limit=args.limit)
        print(f"\n📚 Found {len(results)} results for '{args.search}':\n")
        for item in results:
            print(f"  • {item.apa_citation}: {item.title[:60]}...")
    
    elif args.solo_authored:
        results = client.get_solo_authored(limit=args.limit)
        print(f"\n🎤 Solo-authored papers ({len(results)}):\n")
        for item in results:
            print(f"  • {item.year}: {item.title[:60]}...")
    
    elif args.first_authored:
        results = client.get_first_authored(args.first_authored, limit=args.limit)
        print(f"\n📝 First-authored by {args.first_authored} ({len(results)}):\n")
        for item in results:
            print(f"  • {item.year}: {item.title[:60]}...")
    
    elif args.collections:
        cols = client.list_collections()
        print(f"\n📁 Collections ({len(cols)}):\n")
        for col in cols:
            print(f"  • {col['name']}")
    
    else:
        parser.print_help()
