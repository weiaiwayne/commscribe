#!/usr/bin/env python3
"""
Voice Learning Module for 4-Stage Literature Review Pipeline

Extracts user writing style from samples and generates voice-constrained prompts
for Stage 3 (Iterative Drafting) to produce text in the user's voice.

Based on research findings:
- 5-10 samples of 500+ words recommended
- Key features: function words, sentence length variation, hedging patterns
- Multi-tier prompting: characterization → profile → constrained generation
"""

import re
import json
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime
from collections import Counter


@dataclass
class StyleProfile:
    """User's extracted writing style profile"""
    user_id: str
    extracted_at: str
    sample_count: int
    total_words: int
    
    # Lexical features
    type_token_ratio: float
    avg_word_length: float
    vocabulary_richness: float  # hapax legomena ratio
    function_word_dist: Dict[str, float]
    content_word_preferences: List[str]
    
    # Syntactic features
    avg_sentence_length: float
    sentence_length_std: float
    sentence_length_range: Tuple[int, int]
    passive_voice_ratio: float
    question_frequency: float
    
    # Discourse features
    hedge_frequency: float
    hedge_types: List[str]
    transition_frequency: float
    preferred_transitions: List[str]
    paragraph_length_avg: float
    paragraph_length_std: float
    
    # Academic features
    citation_density: float  # citations per 100 words
    first_person_usage: float  # I/we frequency
    
    # Generated prompt components
    style_description: str
    generation_constraints: str


@dataclass 
class VoiceValidation:
    """Validation results for voice matching"""
    similarity_score: float  # 0-1, how well output matches user voice
    ai_detection_risk: float  # 0-1, likelihood of AI detection
    feature_deviations: Dict[str, float]
    suggestions: List[str]
    passed: bool


class StyleProfileExtractor:
    """
    Extracts comprehensive style profile from user writing samples.
    Uses statistical analysis + pattern matching for stylometric features.
    """
    
    # Common function words (content-independent style markers)
    FUNCTION_WORDS = [
        'the', 'a', 'an', 'and', 'or', 'but', 'if', 'then', 'because',
        'as', 'until', 'while', 'of', 'at', 'by', 'for', 'with', 'about',
        'to', 'from', 'in', 'on', 'that', 'this', 'which', 'who', 'what',
        'is', 'are', 'was', 'were', 'be', 'been', 'being', 'have', 'has',
        'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should',
        'may', 'might', 'must', 'can', 'i', 'we', 'you', 'he', 'she', 'it',
        'they', 'my', 'our', 'your', 'his', 'her', 'its', 'their'
    ]
    
    # Hedge words (uncertainty markers)
    HEDGE_WORDS = [
        'may', 'might', 'could', 'possibly', 'perhaps', 'probably',
        'likely', 'unlikely', 'suggests', 'indicates', 'appears',
        'seems', 'arguably', 'potentially', 'presumably', 'generally',
        'typically', 'often', 'sometimes', 'occasionally', 'tends'
    ]
    
    # Academic transition words
    TRANSITIONS = [
        'however', 'furthermore', 'moreover', 'consequently', 'therefore',
        'nevertheless', 'nonetheless', 'thus', 'hence', 'accordingly',
        'meanwhile', 'subsequently', 'alternatively', 'conversely',
        'similarly', 'likewise', 'notably', 'specifically', 'particularly',
        'indeed', 'certainly', 'clearly', 'obviously', 'evidently'
    ]
    
    # Generic AI-sounding phrases to avoid
    AI_PATTERNS = [
        r'\bit is important to note\b',
        r'\bit is worth noting\b', 
        r'\bit should be noted\b',
        r'\bin recent years\b',
        r'\bwith the rise of\b',
        r'\bthis paper explores\b',
        r'\bthis study aims to\b',
        r'\bin conclusion\b',
        r'\bin summary\b',
        r'\bfirstly.*secondly.*thirdly\b',
    ]
    
    def __init__(self):
        self.samples: List[str] = []
        self.profile: Optional[StyleProfile] = None
    
    def add_sample(self, text: str) -> None:
        """Add a writing sample for analysis"""
        if len(text.split()) >= 100:  # Minimum viable sample
            self.samples.append(text)
    
    def add_samples_from_files(self, file_paths: List[Path]) -> int:
        """Load samples from text/markdown files"""
        loaded = 0
        for path in file_paths:
            try:
                text = path.read_text(encoding='utf-8')
                self.add_sample(text)
                loaded += 1
            except Exception as e:
                print(f"Warning: Could not load {path}: {e}")
        return loaded
    
    def extract_profile(self, user_id: str) -> StyleProfile:
        """Extract comprehensive style profile from all samples"""
        if not self.samples:
            raise ValueError("No samples loaded. Add samples before extracting profile.")
        
        all_text = ' '.join(self.samples)
        words = self._tokenize_words(all_text)
        sentences = self._tokenize_sentences(all_text)
        paragraphs = self._tokenize_paragraphs(all_text)
        
        # Lexical features
        ttr = self._type_token_ratio(words)
        avg_word_len = np.mean([len(w) for w in words])
        vocab_richness = self._hapax_legomena_ratio(words)
        func_word_dist = self._function_word_distribution(words)
        content_prefs = self._content_word_preferences(words)
        
        # Syntactic features
        sent_lengths = [len(self._tokenize_words(s)) for s in sentences]
        avg_sent_len = np.mean(sent_lengths)
        sent_len_std = np.std(sent_lengths)
        sent_len_range = (min(sent_lengths), max(sent_lengths))
        passive_ratio = self._passive_voice_ratio(sentences)
        question_freq = sum(1 for s in sentences if s.strip().endswith('?')) / len(sentences)
        
        # Discourse features
        hedge_freq = self._marker_frequency(words, self.HEDGE_WORDS)
        hedge_types = self._get_used_markers(words, self.HEDGE_WORDS)
        trans_freq = self._marker_frequency(words, self.TRANSITIONS)
        pref_transitions = self._get_used_markers(words, self.TRANSITIONS)
        para_lengths = [len(self._tokenize_words(p)) for p in paragraphs if p.strip()]
        para_avg = np.mean(para_lengths) if para_lengths else 150
        para_std = np.std(para_lengths) if para_lengths else 50
        
        # Academic features
        citation_density = self._citation_density(all_text, words)
        first_person = self._first_person_usage(words)
        
        # Generate prompts
        style_desc = self._generate_style_description(
            avg_sent_len, sent_len_std, passive_ratio, hedge_freq, 
            trans_freq, ttr, first_person
        )
        constraints = self._generate_constraints(
            avg_sent_len, sent_len_std, hedge_types, pref_transitions,
            passive_ratio, para_avg
        )
        
        self.profile = StyleProfile(
            user_id=user_id,
            extracted_at=datetime.now().isoformat(),
            sample_count=len(self.samples),
            total_words=len(words),
            type_token_ratio=round(ttr, 3),
            avg_word_length=round(avg_word_len, 2),
            vocabulary_richness=round(vocab_richness, 3),
            function_word_dist={k: round(v, 4) for k, v in list(func_word_dist.items())[:20]},
            content_word_preferences=content_prefs[:15],
            avg_sentence_length=round(avg_sent_len, 1),
            sentence_length_std=round(sent_len_std, 1),
            sentence_length_range=sent_len_range,
            passive_voice_ratio=round(passive_ratio, 3),
            question_frequency=round(question_freq, 3),
            hedge_frequency=round(hedge_freq, 4),
            hedge_types=hedge_types[:10],
            transition_frequency=round(trans_freq, 4),
            preferred_transitions=pref_transitions[:10],
            paragraph_length_avg=round(para_avg, 1),
            paragraph_length_std=round(para_std, 1),
            citation_density=round(citation_density, 3),
            first_person_usage=round(first_person, 4),
            style_description=style_desc,
            generation_constraints=constraints
        )
        
        return self.profile
    
    def _tokenize_words(self, text: str) -> List[str]:
        """Simple word tokenization"""
        return re.findall(r'\b[a-zA-Z]+\b', text.lower())
    
    def _tokenize_sentences(self, text: str) -> List[str]:
        """Split into sentences"""
        return re.split(r'(?<=[.!?])\s+', text)
    
    def _tokenize_paragraphs(self, text: str) -> List[str]:
        """Split into paragraphs"""
        return re.split(r'\n\s*\n', text)
    
    def _type_token_ratio(self, words: List[str]) -> float:
        """Vocabulary diversity measure"""
        if not words:
            return 0
        return len(set(words)) / len(words)
    
    def _hapax_legomena_ratio(self, words: List[str]) -> float:
        """Ratio of words appearing only once (vocabulary richness)"""
        if not words:
            return 0
        counts = Counter(words)
        hapax = sum(1 for w, c in counts.items() if c == 1)
        return hapax / len(set(words))
    
    def _function_word_distribution(self, words: List[str]) -> Dict[str, float]:
        """Distribution of function words"""
        total = len(words)
        if not total:
            return {}
        counts = Counter(words)
        return {w: counts.get(w, 0) / total for w in self.FUNCTION_WORDS}
    
    def _content_word_preferences(self, words: List[str]) -> List[str]:
        """Most frequent content words (excluding function words)"""
        func_set = set(self.FUNCTION_WORDS)
        content = [w for w in words if w not in func_set and len(w) > 3]
        counts = Counter(content)
        return [w for w, _ in counts.most_common(30)]
    
    def _passive_voice_ratio(self, sentences: List[str]) -> float:
        """Estimate passive voice usage"""
        passive_patterns = [
            r'\b(is|are|was|were|be|been|being)\s+\w+ed\b',
            r'\b(is|are|was|were|be|been|being)\s+\w+en\b',
        ]
        passive_count = 0
        for sent in sentences:
            for pattern in passive_patterns:
                if re.search(pattern, sent.lower()):
                    passive_count += 1
                    break
        return passive_count / len(sentences) if sentences else 0
    
    def _marker_frequency(self, words: List[str], markers: List[str]) -> float:
        """Frequency of marker words per 100 words"""
        if not words:
            return 0
        marker_set = set(markers)
        count = sum(1 for w in words if w in marker_set)
        return (count / len(words)) * 100
    
    def _get_used_markers(self, words: List[str], markers: List[str]) -> List[str]:
        """Get markers actually used, sorted by frequency"""
        marker_set = set(markers)
        used = [w for w in words if w in marker_set]
        counts = Counter(used)
        return [w for w, _ in counts.most_common()]
    
    def _citation_density(self, text: str, words: List[str]) -> float:
        """Citations per 100 words"""
        # Match common citation patterns: (Author, Year), Author (Year), [1], etc.
        patterns = [
            r'\([A-Z][a-z]+(?:\s+(?:&|and)\s+[A-Z][a-z]+)?,?\s*\d{4}\)',
            r'[A-Z][a-z]+\s+\(\d{4}\)',
            r'\[\d+\]',
            r'\(\d{4}\)',
        ]
        total_citations = 0
        for pattern in patterns:
            total_citations += len(re.findall(pattern, text))
        return (total_citations / len(words)) * 100 if words else 0
    
    def _first_person_usage(self, words: List[str]) -> float:
        """Frequency of first-person pronouns"""
        if not words:
            return 0
        first_person = {'i', 'we', 'my', 'our', 'me', 'us', 'myself', 'ourselves'}
        count = sum(1 for w in words if w in first_person)
        return (count / len(words)) * 100
    
    def _generate_style_description(self, avg_sent: float, sent_std: float,
                                     passive: float, hedge: float, trans: float,
                                     ttr: float, first_person: float) -> str:
        """Generate human-readable style description"""
        
        # Sentence complexity
        if avg_sent > 25:
            sent_desc = "complex, lengthy sentences"
        elif avg_sent < 15:
            sent_desc = "concise, punchy sentences"
        else:
            sent_desc = "moderately complex sentences"
        
        # Variation
        if sent_std > 10:
            var_desc = "with high variation in length"
        elif sent_std < 5:
            var_desc = "with consistent, uniform length"
        else:
            var_desc = "with moderate variation"
        
        # Voice
        if passive > 0.3:
            voice_desc = "predominantly passive voice"
        elif passive < 0.1:
            voice_desc = "predominantly active voice"
        else:
            voice_desc = "balanced active/passive voice"
        
        # Hedging
        if hedge > 2.0:
            hedge_desc = "frequent hedging and uncertainty markers"
        elif hedge < 0.5:
            hedge_desc = "direct, confident claims with minimal hedging"
        else:
            hedge_desc = "moderate use of hedging language"
        
        # Vocabulary
        if ttr > 0.5:
            vocab_desc = "rich, varied vocabulary"
        elif ttr < 0.3:
            vocab_desc = "focused, repetitive vocabulary"
        else:
            vocab_desc = "moderately diverse vocabulary"
        
        # Person
        if first_person > 1.5:
            person_desc = "strong authorial presence (frequent I/we)"
        elif first_person < 0.3:
            person_desc = "impersonal, objective tone"
        else:
            person_desc = "balanced personal/impersonal voice"
        
        return f"""Writing style characterized by {sent_desc} {var_desc}. 
Uses {voice_desc} with {hedge_desc}. 
Features {vocab_desc} and {person_desc}."""
    
    def _generate_constraints(self, avg_sent: float, sent_std: float,
                               hedges: List[str], transitions: List[str],
                               passive: float, para_avg: float) -> str:
        """Generate specific constraints for LLM generation"""
        
        hedge_str = ', '.join(hedges[:5]) if hedges else 'suggests, indicates, appears'
        trans_str = ', '.join(transitions[:5]) if transitions else 'however, furthermore'
        
        return f"""VOICE CONSTRAINTS:
1. Sentence length: Target {avg_sent:.0f} words (±{sent_std:.0f}), vary between {max(8, avg_sent-sent_std*2):.0f}-{avg_sent+sent_std*2:.0f}
2. Paragraph length: Approximately {para_avg:.0f} words per paragraph
3. Passive voice: Use in approximately {passive*100:.0f}% of sentences
4. Hedging: Use hedges like "{hedge_str}" approximately every {100/max(0.5, avg_sent/10):.0f} sentences
5. Transitions: Prefer "{trans_str}" over generic "furthermore, moreover, additionally"
6. Avoid: "It is important to note", "In recent years", "This paper explores"
7. DO NOT use numbered lists or bullet points unless the user's samples contain them
8. Mirror the level of formality and directness from the samples"""
    
    def save_profile(self, output_path: Path) -> None:
        """Save profile to JSON file"""
        if not self.profile:
            raise ValueError("No profile extracted yet")
        
        with open(output_path, 'w') as f:
            json.dump(asdict(self.profile), f, indent=2)
    
    def load_profile(self, input_path: Path) -> StyleProfile:
        """Load profile from JSON file"""
        with open(input_path, 'r') as f:
            data = json.load(f)
        
        # Convert tuple back
        data['sentence_length_range'] = tuple(data['sentence_length_range'])
        self.profile = StyleProfile(**data)
        return self.profile


class VoicePromptGenerator:
    """
    Generates prompts that inject user voice into LLM generation.
    Uses multi-tier prompting: characterization → profile → constrained generation
    Now includes anti-AI pattern avoidance instructions.
    """
    
    def __init__(self, profile: StyleProfile, samples: List[str] = None):
        self.profile = profile
        self.samples = samples or []
        
        # Import anti-AI patterns
        try:
            from anti_ai_patterns import generate_avoidance_prompt
            self.anti_ai_prompt = generate_avoidance_prompt(include_examples=True, compact=False)
            self.anti_ai_compact = generate_avoidance_prompt(compact=True)
        except ImportError:
            # Fallback if module not found
            self.anti_ai_prompt = self._fallback_anti_ai_prompt()
            self.anti_ai_compact = self.anti_ai_prompt
    
    def _fallback_anti_ai_prompt(self) -> str:
        """Fallback anti-AI instructions if module not available"""
        return """## ANTI-AI WRITING INSTRUCTIONS

DO NOT USE these AI-typical patterns:
- "In recent years", "In today's world", "With the rise of"
- "It is important to note that", "It should be noted that"
- "Furthermore", "Moreover", "Additionally" (overused)
- "a wide range of", "plays a crucial role in"
- "In conclusion", "To summarize", "All in all"
- Excessive hedging: "could potentially", "might possibly"
- Emoji in academic text: 🔑💡✨

INSTEAD:
- Start with specifics (name years, researchers, numbers)
- Show, don't announce importance
- Use concrete data: "increased 40%" not "significantly increased"
- Vary sentence length naturally
- Let logic drive transitions
"""
    
    def generate_voice_prompt(self, include_examples: bool = True, 
                               include_anti_ai: bool = True) -> str:
        """Generate complete voice injection prompt with anti-AI instructions"""
        
        parts = []
        
        # Tier 0: Anti-AI patterns (if enabled)
        if include_anti_ai:
            parts.append(self.anti_ai_compact if not include_examples else self.anti_ai_prompt)
            parts.append("\n---\n")
        
        # Tier 1: Voice characterization
        parts.append(f"""## VOICE CHARACTERIZATION

{self.profile.style_description}

Key stylistic features:
- Average sentence length: {self.profile.avg_sentence_length} words (std: {self.profile.sentence_length_std})
- Vocabulary richness (TTR): {self.profile.type_token_ratio}
- Passive voice usage: {self.profile.passive_voice_ratio*100:.1f}%
- Hedging frequency: {self.profile.hedge_frequency:.2f} per 100 words
- Preferred hedges: {', '.join(self.profile.hedge_types[:5])}
- Preferred transitions: {', '.join(self.profile.preferred_transitions[:5])}
- First-person usage: {self.profile.first_person_usage:.2f} per 100 words
- Citation density: {self.profile.citation_density:.2f} per 100 words""")
        
        # Tier 2: Explicit constraints
        parts.append(f"""
## GENERATION CONSTRAINTS

{self.profile.generation_constraints}""")
        
        # Tier 3: Few-shot examples (if available)
        if include_examples and self.samples:
            parts.append("""
## WRITING EXAMPLES (Match this voice)

""")
            for i, sample in enumerate(self.samples[:3], 1):
                # Take first ~300 words of each sample
                excerpt = ' '.join(sample.split()[:300])
                parts.append(f"### Example {i}:\n{excerpt}\n\n---\n")
        
        return '\n'.join(parts)
    
    def wrap_generation_request(self, content_request: str, 
                                  voice_prompt: str = None,
                                  include_anti_ai: bool = True) -> str:
        """Wrap a content request with voice constraints and anti-AI instructions"""
        
        if voice_prompt is None:
            voice_prompt = self.generate_voice_prompt(include_anti_ai=include_anti_ai)
        
        return f"""{voice_prompt}

## WRITING TASK

{content_request}

## CRITICAL INSTRUCTIONS

You are writing as if you ARE the author whose samples were provided. Write authentically.

**VOICE MATCHING:**
- Match the sentence length patterns and variation from the profile
- Use the preferred hedging and transition words (not generic ones)
- Maintain the vocabulary richness level
- Follow the formality and directness of the examples

**ANTI-AI REQUIREMENTS (STRICTLY ENFORCED):**
- NEVER use phrases from the anti-AI patterns list above
- NEVER start paragraphs with "In recent years", "It is important to note", etc.
- NEVER use "Furthermore, Moreover, Additionally" in sequence
- NEVER use filler like "a wide range of", "plays a crucial role"
- NEVER conclude with "In conclusion" or "To summarize"
- NO emoji (🔑💡✨) unless the user's samples contain them
- NO numbered lists unless explicitly requested

**POSITIVE REQUIREMENTS:**
- Start sentences with specific subjects, data, or claims
- Use concrete numbers and examples
- Let ideas connect logically without formulaic transitions
- Vary paragraph lengths naturally
- Sound like a specific person, not generic academic-ese

Write naturally as if you were the author of the examples.
"""


class HumanizationLayer:
    """
    Post-processing to reduce AI detectability.
    Based on research: sentence variation, hedge injection, structure variance.
    """
    
    def __init__(self, profile: StyleProfile):
        self.profile = profile
    
    def humanize(self, text: str) -> str:
        """Apply humanization transforms to reduce AI detectability"""
        
        # 1. Inject sentence length variation
        text = self._vary_sentence_lengths(text)
        
        # 2. Replace formulaic transitions
        text = self._replace_generic_transitions(text)
        
        # 3. Remove AI-telltale patterns
        text = self._remove_ai_patterns(text)
        
        # 4. Vary paragraph structure
        text = self._vary_paragraphs(text)
        
        return text
    
    def _vary_sentence_lengths(self, text: str) -> str:
        """Add variation to overly uniform sentences"""
        sentences = re.split(r'(?<=[.!?])\s+', text)
        
        if len(sentences) < 3:
            return text
        
        # Calculate current variation
        lengths = [len(s.split()) for s in sentences]
        current_std = np.std(lengths)
        target_std = self.profile.sentence_length_std
        
        # If too uniform, occasionally combine or split
        if current_std < target_std * 0.5:
            # Combine some short adjacent sentences
            new_sentences = []
            i = 0
            while i < len(sentences):
                if (i + 1 < len(sentences) and 
                    lengths[i] < 12 and lengths[i+1] < 12 and
                    np.random.random() < 0.3):
                    # Combine with semicolon or em-dash
                    connector = np.random.choice(['; ', '—'])
                    combined = sentences[i].rstrip('.!?') + connector + sentences[i+1][0].lower() + sentences[i+1][1:]
                    new_sentences.append(combined)
                    i += 2
                else:
                    new_sentences.append(sentences[i])
                    i += 1
            sentences = new_sentences
        
        return ' '.join(sentences)
    
    def _replace_generic_transitions(self, text: str) -> str:
        """Replace overused AI transitions with user's preferred ones"""
        
        generic_to_preferred = {
            r'\bFurthermore\b': self.profile.preferred_transitions[0] if self.profile.preferred_transitions else 'Moreover',
            r'\bAdditionally\b': 'Also' if 'also' in [t.lower() for t in self.profile.preferred_transitions] else 'In addition',
            r'\bMoreover\b': self.profile.preferred_transitions[1] if len(self.profile.preferred_transitions) > 1 else 'Additionally',
            r'\bIn conclusion\b': 'Overall' if np.random.random() > 0.5 else 'To summarize',
            r'\bIt is important to note that\b': 'Notably',
            r'\bIt should be noted that\b': 'Note that',
        }
        
        for pattern, replacement in generic_to_preferred.items():
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _remove_ai_patterns(self, text: str) -> str:
        """Remove or rephrase obvious AI patterns"""
        
        replacements = [
            (r'In recent years,?\s*', ''),
            (r'With the rise of [^,]+,\s*', ''),
            (r'This paper explores\s*', 'This analysis examines '),
            (r'It is widely acknowledged that\s*', ''),
            (r'It is worth mentioning that\s*', ''),
            (r'plays a (crucial|vital|important) role', 'matters'),
        ]
        
        for pattern, replacement in replacements:
            text = re.sub(pattern, replacement, text, flags=re.IGNORECASE)
        
        return text
    
    def _vary_paragraphs(self, text: str) -> str:
        """Ensure paragraph lengths have natural variation"""
        paragraphs = text.split('\n\n')
        
        # Check if paragraphs are too uniform
        lengths = [len(p.split()) for p in paragraphs if p.strip()]
        if not lengths:
            return text
        
        current_std = np.std(lengths)
        target_std = self.profile.paragraph_length_std
        
        # If needed, we could split or combine paragraphs here
        # For now, just return as-is (more aggressive transforms can be added)
        
        return text


def integrate_voice_learning(research_dir: Path = None):
    """
    Integration helper for the 4-stage research pipeline.
    Returns functions that can be called from the main pipeline.
    """
    
    if research_dir is None:
        research_dir = Path('/root/clawd/research')
    
    profiles_dir = research_dir / 'voice_profiles'
    profiles_dir.mkdir(exist_ok=True)
    
    def extract_user_voice(user_id: str, sample_texts: List[str]) -> StyleProfile:
        """Extract and save voice profile from user samples"""
        extractor = StyleProfileExtractor()
        for text in sample_texts:
            extractor.add_sample(text)
        
        profile = extractor.extract_profile(user_id)
        
        # Save profile
        profile_path = profiles_dir / f'{user_id}_voice_profile.json'
        extractor.save_profile(profile_path)
        
        return profile
    
    def load_user_voice(user_id: str) -> Optional[StyleProfile]:
        """Load existing voice profile"""
        profile_path = profiles_dir / f'{user_id}_voice_profile.json'
        if not profile_path.exists():
            return None
        
        extractor = StyleProfileExtractor()
        return extractor.load_profile(profile_path)
    
    def generate_voiced_prompt(profile: StyleProfile, 
                                content_request: str,
                                samples: List[str] = None) -> str:
        """Generate voice-constrained prompt for drafting"""
        generator = VoicePromptGenerator(profile, samples)
        return generator.wrap_generation_request(content_request)
    
    def humanize_output(profile: StyleProfile, text: str) -> str:
        """Post-process to reduce AI detectability"""
        humanizer = HumanizationLayer(profile)
        return humanizer.humanize(text)
    
    return {
        'extract': extract_user_voice,
        'load': load_user_voice,
        'prompt': generate_voiced_prompt,
        'humanize': humanize_output,
    }


# Command-line interface for testing
if __name__ == '__main__':
    import sys
    
    print("=" * 60)
    print("Voice Learning Module - Test Mode")
    print("=" * 60)
    
    # Test with sample academic text
    test_samples = [
        """
        This study examines the evolution of networked gatekeeping in digital media 
        environments. Drawing on Meraz and Papacharissi's (2013) framework, we argue 
        that traditional gatekeeping models inadequately capture the distributed nature 
        of information control in social media contexts. Our analysis suggests that 
        algorithmic curation, user sharing behaviors, and platform affordances interact 
        to create emergent gatekeeping dynamics that differ substantially from legacy 
        media structures. However, we note several limitations in existing approaches.
        The findings indicate that power relations remain central to understanding 
        information flows, even as the mechanisms of control have shifted. We conclude 
        by proposing a multi-level framework that accounts for both human and algorithmic
        agency in contemporary gatekeeping processes.
        """,
        """
        The relationship between social media platforms and democratic discourse has 
        been extensively debated in recent scholarship. While some researchers emphasize 
        the democratizing potential of networked communication (Bennett & Segerberg, 2012),
        others highlight the risks of fragmentation and echo chambers (Sunstein, 2017).
        Our approach synthesizes these perspectives by examining how platform architecture
        shapes the conditions of possibility for public deliberation. We find that 
        algorithmic feeds neither uniformly enhance nor undermine democratic engagement;
        rather, their effects are contingent on user behavior patterns and content 
        characteristics. This suggests that platform governance interventions should 
        be targeted and context-sensitive rather than uniform.
        """
    ]
    
    # Extract profile
    extractor = StyleProfileExtractor()
    for sample in test_samples:
        extractor.add_sample(sample)
    
    profile = extractor.extract_profile("test_user")
    
    print("\n📊 EXTRACTED STYLE PROFILE")
    print("-" * 40)
    print(f"Samples analyzed: {profile.sample_count}")
    print(f"Total words: {profile.total_words}")
    print(f"\nSentence length: {profile.avg_sentence_length} (±{profile.sentence_length_std})")
    print(f"Type-token ratio: {profile.type_token_ratio}")
    print(f"Passive voice: {profile.passive_voice_ratio*100:.1f}%")
    print(f"Hedge frequency: {profile.hedge_frequency:.2f}/100 words")
    print(f"Preferred hedges: {', '.join(profile.hedge_types[:5])}")
    print(f"First person: {profile.first_person_usage:.2f}/100 words")
    
    print("\n📝 STYLE DESCRIPTION")
    print("-" * 40)
    print(profile.style_description)
    
    print("\n⚙️ GENERATION CONSTRAINTS")
    print("-" * 40)
    print(profile.generation_constraints)
    
    # Generate voice prompt
    generator = VoicePromptGenerator(profile, test_samples)
    voice_prompt = generator.generate_voice_prompt(include_examples=False)
    
    print("\n🎤 VOICE PROMPT (preview)")
    print("-" * 40)
    print(voice_prompt[:1000] + "...")
    
    print("\n✅ Voice learning module ready for integration")
