#!/usr/bin/env python3
"""
Anti-AI Writing Patterns Module

Comprehensive catalog of phrases, structures, and patterns commonly found in AI-generated
text. Used to instruct LLMs to AVOID these patterns during generation.

Based on:
- AI detector research (GPTZero, Originality.ai analysis)
- Kumar et al. (2023) - AI text detection signals
- Liang et al. (2024) - LLM patterns in scientific papers
- Community observations from r/ChatGPT, academic Twitter
"""

from typing import List, Dict
from dataclasses import dataclass


@dataclass
class PatternCategory:
    """Category of AI writing patterns to avoid"""
    name: str
    description: str
    patterns: List[str]
    examples_bad: List[str]  # AI-typical examples
    examples_good: List[str]  # Human-like alternatives


# =============================================================================
# COMPREHENSIVE AI PATTERN CATALOG
# =============================================================================

OPENER_PHRASES = PatternCategory(
    name="Generic Openers",
    description="AI loves to start paragraphs/sections with these formulaic phrases",
    patterns=[
        "In today's [world/society/age]",
        "In recent years",
        "In the realm of",
        "In the world of",
        "In the context of",
        "In the field of",
        "In this day and age",
        "Throughout history",
        "Since the dawn of time",
        "As we navigate",
        "As we delve into",
        "As technology continues to evolve",
        "With the rise of",
        "With the advent of",
        "With the increasing importance of",
        "Given the importance of",
        "When it comes to",
        "When we think about",
        "It is no secret that",
        "It goes without saying that",
        "It is widely acknowledged that",
        "It is commonly known that",
        "It is well established that",
    ],
    examples_bad=[
        "In today's rapidly evolving digital landscape...",
        "In recent years, social media has become increasingly important...",
        "As we navigate the complexities of modern communication...",
    ],
    examples_good=[
        "Social media platforms now mediate most political discourse.",
        "Twitter's algorithmic feed, introduced in 2016, fundamentally changed...",
        "The 2020 election revealed how quickly misinformation spreads.",
    ]
)

IMPORTANCE_PHRASES = PatternCategory(
    name="Importance/Noting Phrases",
    description="AI constantly tells readers what's important instead of showing",
    patterns=[
        "It is important to note that",
        "It is worth noting that",
        "It should be noted that",
        "It is crucial to understand that",
        "It is essential to recognize that",
        "It is vital to consider that",
        "It bears mentioning that",
        "It must be emphasized that",
        "It cannot be overstated that",
        "Importantly,",
        "Notably,",
        "Crucially,",
        "Significantly,",
        "Interestingly,",  # When overused
        "Remarkably,",
        "Strikingly,",
        "What's important here is",
        "The key point is that",
        "The crucial aspect is",
        "One important thing to consider is",
    ],
    examples_bad=[
        "It is important to note that gatekeeping has evolved significantly.",
        "Crucially, this demonstrates the limitations of traditional models.",
        "It cannot be overstated that algorithmic curation matters.",
    ],
    examples_good=[
        "Gatekeeping has evolved from editorial control to algorithmic curation.",
        "This limitation—the inability to track intent—undermines causal claims.",
        "Algorithmic curation now determines what 70% of users see first.",
    ]
)

TRANSITION_OVERUSE = PatternCategory(
    name="Overused Transitions",
    description="AI relies heavily on a small set of formal transitions",
    patterns=[
        "Furthermore,",
        "Moreover,",
        "Additionally,",
        "In addition,",
        "Consequently,",
        "Subsequently,",
        "Thus,",
        "Hence,",
        "Therefore,",
        "Accordingly,",
        "As a result,",
        "In conclusion,",
        "To summarize,",
        "In summary,",
        "To sum up,",
        "All in all,",
        "On the other hand,",
        "Conversely,",
        "Nevertheless,",
        "Nonetheless,",
        "That being said,",
        "With that said,",
        "Having said that,",
        "That said,",
        "Be that as it may,",
        "First and foremost,",
        "Last but not least,",
        "Firstly, ... Secondly, ... Thirdly,",
    ],
    examples_bad=[
        "Furthermore, this approach has several advantages. Moreover, it addresses...",
        "In conclusion, the evidence suggests that...",
        "Firstly, we examine... Secondly, we analyze... Thirdly, we discuss...",
    ],
    examples_good=[
        "This approach also addresses the scalability concern.",
        "The evidence points to algorithmic amplification as the key mechanism.",
        "We begin with the data, then turn to methods, and finally interpret results.",
    ]
)

HEDGE_OVERLOAD = PatternCategory(
    name="Excessive Hedging",
    description="AI hedges constantly, making text sound uncertain and generic",
    patterns=[
        "may or may not",
        "could potentially",
        "might possibly",
        "to some extent",
        "in some ways",
        "in certain respects",
        "to a certain degree",
        "arguably",
        "perhaps",
        "possibly",
        "potentially",
        "seemingly",
        "apparently",
        "it seems that",
        "it appears that",
        "it would seem that",
        "one could argue that",
        "some might say that",
        "there is a possibility that",
        "it is possible that",
        "it is likely that",
        "tends to",
        "has the potential to",
    ],
    examples_bad=[
        "This could potentially have significant implications for...",
        "It would seem that there is a possibility that users might...",
        "One could argue that this approach arguably has some merit.",
    ],
    examples_good=[
        "This implies that platform design shapes user behavior.",
        "Users in treatment groups shared 40% more misinformation.",
        "This approach works for short-form content but fails for nuanced topics.",
    ]
)

FILLER_PHRASES = PatternCategory(
    name="Filler/Padding Phrases",
    description="Empty phrases that add words without meaning",
    patterns=[
        "a wide range of",
        "a variety of",
        "a plethora of",
        "a myriad of",
        "a multitude of",
        "an array of",
        "a vast array of",
        "countless",
        "numerous",
        "innumerable",
        "various",
        "diverse",
        "different",  # When vague
        "many different",
        "several key",
        "multiple",
        "serves as",
        "acts as",
        "functions as",
        "plays a role in",
        "plays a crucial role in",
        "plays a vital role in",
        "plays an important role in",
        "is considered to be",
        "can be seen as",
        "is known to be",
        "is said to be",
        "in terms of",
        "with regard to",
        "with respect to",
        "in relation to",
        "pertaining to",
        "regarding",
        "concerning",
        "the fact that",
        "due to the fact that",
        "owing to the fact that",
        "despite the fact that",
        "in light of the fact that",
        "given the fact that",
    ],
    examples_bad=[
        "A wide range of factors play a crucial role in determining outcomes.",
        "Due to the fact that users have various different preferences...",
        "This serves as an important example of the phenomenon in question.",
    ],
    examples_good=[
        "Three factors determine outcomes: reach, timing, and source credibility.",
        "Because user preferences vary...",
        "This example shows how amplification works.",
    ]
)

STRUCTURE_PATTERNS = PatternCategory(
    name="Structural Patterns",
    description="Predictable structures that signal AI generation",
    patterns=[
        "Let's dive in",
        "Let's explore",
        "Let's delve into",
        "Let's take a closer look",
        "Let's examine",
        "Let's unpack",
        "Let me explain",
        "Allow me to",
        "I'd be happy to",
        "Great question!",
        "That's a great question",
        "Absolutely!",
        "Certainly!",
        "Of course!",
        "Here's the thing:",
        "Here's what you need to know:",
        "The bottom line is",
        "At the end of the day",
        "When all is said and done",
        "Moving forward",
        "Going forward",
        "Looking ahead",
        # List obsession
        "Here are [N] reasons/ways/tips",
        "There are several key points",
        "Consider the following:",
        "The following points illustrate",
    ],
    examples_bad=[
        "Let's dive into the complexities of networked gatekeeping!",
        "Great question! Here are 5 key points to consider:",
        "At the end of the day, what matters is...",
    ],
    examples_good=[
        "Networked gatekeeping differs from traditional models in three ways.",
        "The central tension is between reach and accuracy.",
        "Ultimately, platform architecture constrains what's possible.",
    ]
)

ADJECTIVE_INFLATION = PatternCategory(
    name="Inflated Adjectives",
    description="AI loves superlatives and intensifiers that weaken prose",
    patterns=[
        "very",
        "really",
        "extremely",
        "incredibly",
        "absolutely",
        "utterly",
        "completely",
        "totally",
        "highly",
        "deeply",
        "profoundly",
        "significantly",  # When vague
        "substantially",
        "considerably",
        "remarkably",
        "exceptionally",
        "extraordinarily",
        "groundbreaking",
        "revolutionary",
        "transformative",
        "game-changing",
        "cutting-edge",
        "state-of-the-art",
        "world-class",
        "best-in-class",
        "robust",  # Overused in AI
        "comprehensive",  # Overused
        "holistic",
        "synergistic",
        "innovative",
        "novel",  # When everything is "novel"
        "unique",  # When nothing is truly unique
        "seamless",
        "seamlessly",
        "effortless",
        "effortlessly",
    ],
    examples_bad=[
        "This is an extremely comprehensive and highly innovative approach.",
        "The results are truly groundbreaking and absolutely transformative.",
        "We present a novel, robust, and holistic framework.",
    ],
    examples_good=[
        "This approach addresses scalability, which prior methods ignored.",
        "The results show a 3x improvement over the baseline.",
        "We present a framework that handles missing data.",
    ]
)

EMOJI_AND_SYMBOLS = PatternCategory(
    name="Emoji and Symbol Overuse",
    description="AI often inserts emojis and formatting symbols inappropriately",
    patterns=[
        "🔑",  # Key points
        "💡",  # Ideas
        "📌",  # Important
        "✨",  # Emphasis
        "🎯",  # Goals/targets
        "🚀",  # Launch/growth
        "⭐",  # Highlights
        "📊",  # Data
        "🔍",  # Analysis
        "✅",  # Checkmarks in prose
        "❌",  # X marks in prose
        "👉",  # Pointing
        "⚡",  # Energy/speed
        "🌟",  # Star emphasis
        "💪",  # Strength
        "🎉",  # Celebration
        "→",   # Arrows in prose (not diagrams)
        "•",   # Bullets in flowing text
        "—",   # Em-dash overuse (3+ per paragraph)
        "...", # Ellipsis overuse
        "\"\"", # Empty quotes
        "***", # Markdown emphasis overuse
        "###", # Headers in short responses
    ],
    examples_bad=[
        "Key takeaways: 🔑 First, ... 💡 Second, ... ✨ Finally, ...",
        "This is important → it changes everything!",
        "The results were... surprising — to say the least — and transformative.",
    ],
    examples_good=[
        "Three findings stand out. First, ... Second, ... Third, ...",
        "This matters because it changes the incentive structure.",
        "The results surprised us: engagement dropped 40% after the redesign.",
    ]
)

ACADEMIC_AI_PATTERNS = PatternCategory(
    name="Academic AI Patterns",
    description="Patterns specific to AI-generated academic/research writing",
    patterns=[
        "This paper explores",
        "This study aims to",
        "This research investigates",
        "The purpose of this study is to",
        "The aim of this paper is to",
        "We aim to contribute to",
        "This work contributes to",
        "fills a gap in the literature",
        "addresses a gap in",
        "contributes to our understanding of",
        "sheds light on",
        "provides insights into",
        "offers a nuanced understanding of",
        "provides a comprehensive overview of",
        "presents a systematic analysis of",
        "adopts a mixed-methods approach",
        "employs a qualitative methodology",
        "utilizes a quantitative framework",
        "draws on [theory] to argue",
        "building on the work of",
        "extending the work of",
        "in line with previous research",
        "consistent with prior studies",
        "contrary to expectations",
        "as expected",
        "as hypothesized",
        "the findings suggest that",
        "the results indicate that",
        "the data reveal that",
        "our analysis shows that",
        "we find that",
        "we observe that",
        "we note that",
        "future research should",
        "further research is needed",
        "more research is warranted",
        "limitations notwithstanding",
        "despite these limitations",
    ],
    examples_bad=[
        "This paper aims to fill a gap in the literature by providing a comprehensive analysis.",
        "Building on the work of Smith (2020), this study contributes to our understanding.",
        "The findings suggest that, consistent with prior research, the effect is significant.",
    ],
    examples_good=[
        "Prior work assumes static networks; we model temporal evolution.",
        "Smith (2020) focused on broadcast media; we extend this to algorithmic feeds.",
        "The effect size (d=0.4) matches laboratory studies but exceeds field estimates.",
    ]
)

CONCLUSION_CLICHES = PatternCategory(
    name="Conclusion Clichés",
    description="Formulaic ways AI ends sections or papers",
    patterns=[
        "In conclusion,",
        "To conclude,",
        "In summary,",
        "To summarize,",
        "To sum up,",
        "In closing,",
        "Finally,",  # When starting conclusion
        "All in all,",
        "Taken together,",
        "Overall,",  # When overused
        "In the final analysis,",
        "At the end of the day,",
        "When all is said and done,",
        "The bottom line is",
        "What this means is",
        "The takeaway is",
        "The key takeaway is",
        "What we can learn from this is",
        "This goes to show that",
        "This demonstrates that",
        "This highlights the importance of",
        "This underscores the need for",
        "Moving forward,",
        "Going forward,",
        "Looking ahead,",
        "As we move forward,",
        "only time will tell",
        "remains to be seen",
        "the jury is still out",
    ],
    examples_bad=[
        "In conclusion, this paper has demonstrated the importance of gatekeeping.",
        "All in all, the findings underscore the need for further research.",
        "Moving forward, it remains to be seen how platforms will respond.",
    ],
    examples_good=[
        "Gatekeeping has shifted from editors to algorithms—but power remains concentrated.",
        "These three mechanisms—amplification, suppression, and friction—explain 80% of variance.",
        "Platforms will likely respond with more opaque curation, not less.",
    ]
)


# =============================================================================
# AGGREGATE PATTERN LISTS
# =============================================================================

ALL_CATEGORIES = [
    OPENER_PHRASES,
    IMPORTANCE_PHRASES,
    TRANSITION_OVERUSE,
    HEDGE_OVERLOAD,
    FILLER_PHRASES,
    STRUCTURE_PATTERNS,
    ADJECTIVE_INFLATION,
    EMOJI_AND_SYMBOLS,
    ACADEMIC_AI_PATTERNS,
    CONCLUSION_CLICHES,
]


def get_all_patterns() -> List[str]:
    """Get flat list of all patterns to avoid"""
    patterns = []
    for category in ALL_CATEGORIES:
        patterns.extend(category.patterns)
    return patterns


def get_patterns_by_category() -> Dict[str, List[str]]:
    """Get patterns organized by category"""
    return {cat.name: cat.patterns for cat in ALL_CATEGORIES}


def generate_avoidance_prompt(include_examples: bool = True, 
                               compact: bool = False) -> str:
    """
    Generate comprehensive prompt instructing LLM to avoid AI patterns.
    
    Args:
        include_examples: Include bad/good examples for each category
        compact: Generate shorter version with just pattern lists
    
    Returns:
        Prompt string to prepend to generation requests
    """
    
    if compact:
        return _generate_compact_prompt()
    else:
        return _generate_full_prompt(include_examples)


def _generate_compact_prompt() -> str:
    """Short version - just the patterns"""
    
    lines = [
        "## ANTI-AI WRITING PATTERNS",
        "",
        "**DO NOT USE these phrases and patterns** (they signal AI-generated text):",
        "",
    ]
    
    for category in ALL_CATEGORIES:
        lines.append(f"### {category.name}")
        # Take top 10 patterns from each category
        for pattern in category.patterns[:10]:
            lines.append(f"- ❌ {pattern}")
        lines.append("")
    
    lines.extend([
        "## INSTEAD:",
        "- Start sentences with specific subjects, not generic openers",
        "- Show, don't tell (skip 'it is important to note')",
        "- Use concrete numbers and examples",
        "- Vary sentence length naturally",
        "- Let transitions emerge from logic, not formulas",
    ])
    
    return '\n'.join(lines)


def _generate_full_prompt(include_examples: bool) -> str:
    """Full version with explanations and examples"""
    
    lines = [
        "## ANTI-AI WRITING INSTRUCTIONS",
        "",
        "You are writing academic/research content. AI-generated text has recognizable patterns.",
        "To write authentically, you MUST avoid these patterns.",
        "",
        "---",
        "",
    ]
    
    for category in ALL_CATEGORIES:
        lines.append(f"### ❌ AVOID: {category.name}")
        lines.append(f"*{category.description}*")
        lines.append("")
        lines.append("**Patterns to avoid:**")
        
        for pattern in category.patterns:
            lines.append(f"- {pattern}")
        
        if include_examples and category.examples_bad:
            lines.append("")
            lines.append("**BAD (AI-typical):**")
            for ex in category.examples_bad:
                lines.append(f"> {ex}")
            
            lines.append("")
            lines.append("**GOOD (human-like):**")
            for ex in category.examples_good:
                lines.append(f"> {ex}")
        
        lines.append("")
        lines.append("---")
        lines.append("")
    
    # Add positive instructions
    lines.extend([
        "## ✅ INSTEAD, DO THIS:",
        "",
        "1. **Start with specifics**: Instead of 'In recent years', name the year. Instead of 'researchers have found', name the researcher.",
        "",
        "2. **Show, don't announce**: Instead of 'It is important to note that X', just state X. The reader will judge importance.",
        "",
        "3. **Use concrete numbers**: Instead of 'significantly increased', say 'increased by 40%'. Instead of 'many users', say '2.3 million users'.",
        "",
        "4. **Vary sentence structure**: Mix short punchy sentences with longer complex ones. Don't start consecutive sentences the same way.",
        "",
        "5. **Let logic drive transitions**: Instead of 'Furthermore, ...Moreover, ...Additionally', let the ideas connect naturally or use 'but', 'and', 'yet', 'so'.",
        "",
        "6. **Be direct about uncertainty**: Instead of 'it could potentially possibly', say 'we don't know' or 'evidence is mixed'.",
        "",
        "7. **Cut filler**: Delete 'a wide range of', 'plays a crucial role in', 'in terms of'. Get to the point.",
        "",
        "8. **Write conclusions that conclude**: Instead of summarizing what you said, tell the reader what it means or what to do.",
        "",
        "9. **No emoji in academic writing**: Unless the user's samples contain them, never use 🔑💡✨ etc.",
        "",
        "10. **Sound like the author**: Match the voice profile, not generic academic-ese.",
    ])
    
    return '\n'.join(lines)


def check_text_for_patterns(text: str) -> Dict[str, List[str]]:
    """
    Check text for AI patterns and return matches.
    Useful for validation/feedback.
    """
    import re
    
    matches = {}
    text_lower = text.lower()
    
    for category in ALL_CATEGORIES:
        category_matches = []
        for pattern in category.patterns:
            # Simple substring check (could be improved with regex)
            pattern_lower = pattern.lower().rstrip(',').rstrip('.')
            if pattern_lower in text_lower:
                category_matches.append(pattern)
        
        if category_matches:
            matches[category.name] = category_matches
    
    return matches


def get_pattern_density(text: str) -> float:
    """
    Calculate AI pattern density (patterns per 100 words).
    Lower is better. Human text typically < 1.0, AI text often > 3.0
    """
    words = len(text.split())
    if words == 0:
        return 0
    
    matches = check_text_for_patterns(text)
    total_matches = sum(len(m) for m in matches.values())
    
    return (total_matches / words) * 100


# =============================================================================
# COMMAND-LINE INTERFACE
# =============================================================================

if __name__ == '__main__':
    import sys
    
    print("=" * 70)
    print("Anti-AI Writing Patterns Module")
    print("=" * 70)
    print()
    
    # Print stats
    total_patterns = len(get_all_patterns())
    print(f"📊 Total patterns catalogued: {total_patterns}")
    print(f"📁 Categories: {len(ALL_CATEGORIES)}")
    print()
    
    for cat in ALL_CATEGORIES:
        print(f"  • {cat.name}: {len(cat.patterns)} patterns")
    
    print()
    print("-" * 70)
    print("COMPACT PROMPT PREVIEW:")
    print("-" * 70)
    print()
    print(generate_avoidance_prompt(compact=True)[:2000])
    print("...")
    print()
    
    # Test pattern detection
    test_text = """
    In recent years, social media has become increasingly important in our society.
    It is important to note that this has significant implications for democracy.
    Furthermore, the findings suggest that users are affected by algorithmic curation.
    Moreover, this potentially could have various different effects on a wide range of outcomes.
    In conclusion, this paper has demonstrated the crucial role of platforms in modern discourse.
    """
    
    print("-" * 70)
    print("PATTERN DETECTION TEST:")
    print("-" * 70)
    print()
    print("Input text (intentionally AI-sounding):")
    print(test_text)
    print()
    
    matches = check_text_for_patterns(test_text)
    density = get_pattern_density(test_text)
    
    print(f"AI Pattern Density: {density:.2f} per 100 words")
    print(f"(Human: <1.0, AI: >3.0)")
    print()
    print("Detected patterns:")
    for category, patterns in matches.items():
        print(f"  {category}:")
        for p in patterns:
            print(f"    ❌ {p}")
    
    print()
    print("✅ Module ready for integration")
