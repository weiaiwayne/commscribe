#!/usr/bin/env python3
"""
Validation Gates for CommScribe

Enforces stage transition requirements:
- Concept stage: 300+ words, 3+ citations, low AI pattern density
- Draft stage: Tiered validation based on publication target
"""

import re
from dataclasses import dataclass
from typing import List, Optional, Tuple
from enum import Enum

# Import anti-AI patterns for density check
try:
    from .anti_ai_patterns import get_pattern_density, check_text_for_patterns
except ImportError:
    from anti_ai_patterns import get_pattern_density, check_text_for_patterns


class ValidationTier(Enum):
    """Validation tiers matching rigor to stakes"""
    NOTES = "notes"           # 🟢 Exploratory - minimal checks
    DRAFT = "draft"           # 🟡 Internal review - moderate checks  
    PUBLICATION = "publication"  # 🔴 Journal submission - full checks


@dataclass
class ConceptValidation:
    """Result of concept validation"""
    passed: bool
    word_count: int
    citation_count: int
    ai_pattern_density: float
    research_question_found: bool
    theoretical_framing_found: bool
    issues: List[str]
    
    def __str__(self) -> str:
        status = "✅ PASSED" if self.passed else "❌ FAILED"
        issues_str = "\n".join(f"  - {i}" for i in self.issues) if self.issues else "  None"
        return f"""{status}

Word count: {self.word_count} (min: 300)
Citations: {self.citation_count} (min: 3)
AI pattern density: {self.ai_pattern_density:.2f}/100 words (max: 1.0)
Research question: {'✓' if self.research_question_found else '✗'}
Theoretical framing: {'✓' if self.theoretical_framing_found else '✗'}

Issues:
{issues_str}"""


@dataclass
class DraftValidation:
    """Result of draft validation"""
    passed: bool
    tier: ValidationTier
    word_count: int
    citation_count: int
    ai_pattern_density: float
    verify_tags_count: int  # [VERIFY] tags
    voice_match_score: Optional[float]  # If voice profile available
    issues: List[str]
    warnings: List[str]
    
    def __str__(self) -> str:
        status = "✅ PASSED" if self.passed else "❌ FAILED"
        tier_emoji = {"notes": "🟢", "draft": "🟡", "publication": "🔴"}[self.tier.value]
        
        issues_str = "\n".join(f"  ❌ {i}" for i in self.issues) if self.issues else "  None"
        warnings_str = "\n".join(f"  ⚠️ {w}" for w in self.warnings) if self.warnings else "  None"
        
        voice_str = f"{self.voice_match_score:.0%}" if self.voice_match_score else "N/A"
        
        return f"""{status} for {tier_emoji} {self.tier.value.upper()} tier

Word count: {self.word_count}
Citations: {self.citation_count}
AI pattern density: {self.ai_pattern_density:.2f}/100 words
[VERIFY] tags: {self.verify_tags_count}
Voice match: {voice_str}

Issues:
{issues_str}

Warnings:
{warnings_str}"""


class ConceptValidator:
    """Validates concept plans before proceeding to synthesis"""
    
    # Citation patterns
    CITATION_PATTERNS = [
        r'\([A-Z][a-z]+(?:\s+(?:&|and)\s+[A-Z][a-z]+)*,?\s*\d{4}\)',  # (Smith, 2020)
        r'[A-Z][a-z]+\s+\(\d{4}\)',  # Smith (2020)
        r'[A-Z][a-z]+\s+et\s+al\.\s*\(\d{4}\)',  # Smith et al. (2020)
        r'\[\d+\]',  # [1]
        r'\(\d{4}\)',  # (2020) - less specific
    ]
    
    # Research question indicators
    RQ_INDICATORS = [
        r'research\s+question',
        r'RQ\d*:?',
        r'we\s+ask',
        r'this\s+study\s+examines',
        r'this\s+paper\s+investigates',
        r'seeks?\s+to\s+understand',
        r'how\s+(?:do|does|can)',
        r'what\s+(?:is|are|explains)',
        r'why\s+(?:do|does)',
    ]
    
    # Theory indicators
    THEORY_INDICATORS = [
        r'theory\s+of',
        r'theoretical\s+(?:framework|lens|perspective)',
        r'drawing\s+on',
        r'building\s+on',
        r'following\s+\w+',
        r'according\s+to\s+\w+',
        r'framework',
        r'conceptualize',
        r'operationalize',
    ]
    
    def __init__(self, 
                 min_words: int = 300,
                 min_citations: int = 3,
                 max_ai_density: float = 1.0):
        self.min_words = min_words
        self.min_citations = min_citations
        self.max_ai_density = max_ai_density
    
    def count_citations(self, text: str) -> int:
        """Count citations in text"""
        all_citations = set()
        for pattern in self.CITATION_PATTERNS:
            matches = re.findall(pattern, text, re.IGNORECASE)
            all_citations.update(matches)
        return len(all_citations)
    
    def has_research_question(self, text: str) -> bool:
        """Check if text contains research question indicators"""
        for pattern in self.RQ_INDICATORS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def has_theoretical_framing(self, text: str) -> bool:
        """Check if text contains theoretical framing"""
        for pattern in self.THEORY_INDICATORS:
            if re.search(pattern, text, re.IGNORECASE):
                return True
        return False
    
    def validate(self, text: str) -> ConceptValidation:
        """Validate concept plan"""
        issues = []
        
        # Word count
        word_count = len(text.split())
        if word_count < self.min_words:
            issues.append(f"Word count ({word_count}) below minimum ({self.min_words})")
        
        # Citation count
        citation_count = self.count_citations(text)
        if citation_count < self.min_citations:
            issues.append(f"Citations ({citation_count}) below minimum ({self.min_citations})")
        
        # AI pattern density
        ai_density = get_pattern_density(text)
        if ai_density > self.max_ai_density:
            issues.append(f"AI pattern density ({ai_density:.2f}) exceeds maximum ({self.max_ai_density})")
        
        # Research question
        has_rq = self.has_research_question(text)
        if not has_rq:
            issues.append("No clear research question detected")
        
        # Theoretical framing
        has_theory = self.has_theoretical_framing(text)
        if not has_theory:
            issues.append("No theoretical framing detected")
        
        return ConceptValidation(
            passed=len(issues) == 0,
            word_count=word_count,
            citation_count=citation_count,
            ai_pattern_density=ai_density,
            research_question_found=has_rq,
            theoretical_framing_found=has_theory,
            issues=issues
        )


class DraftValidator:
    """Validates drafts based on tier"""
    
    # [VERIFY] tag pattern
    VERIFY_PATTERN = r'\[VERIFY[^\]]*\]'
    
    # Tier-specific requirements
    TIER_REQUIREMENTS = {
        ValidationTier.NOTES: {
            "min_words": 100,
            "max_ai_density": 3.0,  # Lenient
            "verify_tags_allowed": True,
            "voice_match_min": None,  # Not required
        },
        ValidationTier.DRAFT: {
            "min_words": 500,
            "max_ai_density": 1.5,
            "verify_tags_allowed": True,
            "voice_match_min": 0.6,
        },
        ValidationTier.PUBLICATION: {
            "min_words": 1000,
            "max_ai_density": 0.5,  # Strict
            "verify_tags_allowed": False,  # Must resolve all
            "voice_match_min": 0.75,
        },
    }
    
    def __init__(self, tier: ValidationTier = ValidationTier.DRAFT):
        self.tier = tier
        self.requirements = self.TIER_REQUIREMENTS[tier]
    
    def count_verify_tags(self, text: str) -> int:
        """Count [VERIFY] tags in text"""
        return len(re.findall(self.VERIFY_PATTERN, text, re.IGNORECASE))
    
    def validate(self, 
                 text: str, 
                 voice_match_score: Optional[float] = None) -> DraftValidation:
        """Validate draft against tier requirements"""
        issues = []
        warnings = []
        
        # Word count
        word_count = len(text.split())
        if word_count < self.requirements["min_words"]:
            issues.append(f"Word count ({word_count}) below tier minimum ({self.requirements['min_words']})")
        
        # Citation count (informational)
        validator = ConceptValidator()
        citation_count = validator.count_citations(text)
        if citation_count < 5:
            warnings.append(f"Low citation density ({citation_count} citations)")
        
        # AI pattern density
        ai_density = get_pattern_density(text)
        if ai_density > self.requirements["max_ai_density"]:
            issues.append(f"AI pattern density ({ai_density:.2f}) exceeds tier maximum ({self.requirements['max_ai_density']})")
        
        # [VERIFY] tags
        verify_count = self.count_verify_tags(text)
        if verify_count > 0 and not self.requirements["verify_tags_allowed"]:
            issues.append(f"Found {verify_count} unresolved [VERIFY] tags (not allowed in {self.tier.value} tier)")
        elif verify_count > 0:
            warnings.append(f"{verify_count} [VERIFY] tags need resolution before publication")
        
        # Voice match
        if voice_match_score is not None:
            min_voice = self.requirements["voice_match_min"]
            if min_voice and voice_match_score < min_voice:
                issues.append(f"Voice match ({voice_match_score:.0%}) below tier minimum ({min_voice:.0%})")
        elif self.requirements["voice_match_min"]:
            warnings.append("No voice profile available for validation")
        
        return DraftValidation(
            passed=len(issues) == 0,
            tier=self.tier,
            word_count=word_count,
            citation_count=citation_count,
            ai_pattern_density=ai_density,
            verify_tags_count=verify_count,
            voice_match_score=voice_match_score,
            issues=issues,
            warnings=warnings
        )


def validate_concept(text: str, 
                     min_words: int = 300,
                     min_citations: int = 3) -> ConceptValidation:
    """Convenience function for concept validation"""
    validator = ConceptValidator(min_words=min_words, min_citations=min_citations)
    return validator.validate(text)


def validate_draft(text: str,
                   tier: str = "draft",
                   voice_match_score: Optional[float] = None) -> DraftValidation:
    """Convenience function for draft validation"""
    tier_enum = ValidationTier(tier.lower())
    validator = DraftValidator(tier=tier_enum)
    return validator.validate(text, voice_match_score)


# CLI
if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("CommScribe Validation - Test Mode")
    print("=" * 60)
    
    # Test concept
    test_concept = """
    This study examines the evolution of networked gatekeeping in digital media 
    environments. Drawing on Meraz and Papacharissi's (2013) framework, we argue 
    that traditional gatekeeping models inadequately capture the distributed nature 
    of information control in social media contexts. 
    
    Our research question asks: How do algorithmic systems reshape gatekeeping 
    dynamics in contemporary media ecosystems?
    
    Building on agenda-setting theory (McCombs & Shaw, 1972) and the theory of 
    networked publics (boyd, 2010), this paper investigates how platform 
    affordances interact with user behavior to create emergent information flows.
    
    The study contributes to communication scholarship by proposing a multi-level 
    framework that accounts for both human and algorithmic agency. We analyze 
    Twitter data from 2020-2023 to empirically test these theoretical propositions.
    """
    
    print("\n📋 CONCEPT VALIDATION")
    print("-" * 40)
    result = validate_concept(test_concept)
    print(result)
    
    # Test draft
    test_draft = """
    Algorithmic feeds have fundamentally restructured how information flows 
    through digital media systems. Where editorial gatekeepers once determined 
    what publics would see, platform algorithms now curate personalized streams 
    based on engagement predictions (Gillespie, 2018). This shift raises critical 
    questions about the nature of gatekeeping in networked environments.
    
    Traditional gatekeeping theory (White, 1950) emphasized the role of individual 
    decision-makers—editors, journalists, producers—who selected which information 
    would pass through institutional channels [VERIFY: exact page number]. However, 
    in contemporary social media contexts, gatekeeping functions are distributed 
    across multiple actors and technical systems.
    
    Recent scholarship has begun to theorize these transformations. Meraz and 
    Papacharissi (2013) introduced the concept of "networked gatekeeping" to 
    capture how traditional and non-traditional media actors interact to shape 
    information flows. Building on this, we argue that algorithmic curation 
    represents a third phase—neither purely institutional nor purely networked, 
    but a hybrid form where platform infrastructure shapes what networked actors 
    can amplify.
    
    The implications extend beyond theoretical refinement. Understanding algorithmic 
    gatekeeping has practical consequences for democratic discourse, media literacy, 
    and platform governance. As Napoli (2019) argues, algorithmic systems introduce 
    new forms of opacity into information filtering processes that may be even less 
    accountable than traditional gatekeeping.
    """
    
    print("\n📝 DRAFT VALIDATION (Draft Tier)")
    print("-" * 40)
    result = validate_draft(test_draft, tier="draft", voice_match_score=0.72)
    print(result)
    
    print("\n📝 DRAFT VALIDATION (Publication Tier)")
    print("-" * 40)
    result = validate_draft(test_draft, tier="publication", voice_match_score=0.72)
    print(result)
    
    print("\n✅ Validation module ready!")
