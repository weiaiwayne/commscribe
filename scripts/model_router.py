#!/usr/bin/env python3
"""
Hybrid Model Router for CommScribe

Dynamically selects the optimal model for each task based on:
- Content complexity analysis
- Urgency requirements (fast vs quality)
- Task type (synthesis, drafting, audit, voice extraction)
- Historical performance data
- Cost/quality trade-offs

Replaces hardcoded model assignments with intelligent routing.
"""

import json
import re
from enum import Enum
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from pathlib import Path
import hashlib
from datetime import datetime


class TaskType(Enum):
    """Types of tasks in the CommScribe pipeline"""
    SYNTHESIS = "synthesis"           # Literature search and synthesis
    DRAFTING = "drafting"             # Voice-constrained writing
    AUDIT = "audit"                   # Critical review
    VOICE_EXTRACTION = "voice_extraction"  # Voice profile creation
    VALIDATION = "validation"         # Concept/draft validation


class ComplexityTier(Enum):
    """Complexity levels for content"""
    LOW = "low"        # Simple, straightforward
    MEDIUM = "medium"  # Moderate complexity
    HIGH = "high"      # Complex, nuanced
    EXTREME = "extreme"  # Highly complex, requires best model


class UrgencyLevel(Enum):
    """Urgency levels affecting model selection"""
    FAST = "fast"      # Optimize for speed
    BALANCED = "balanced"  # Balance speed and quality
    QUALITY = "quality"  # Optimize for quality


@dataclass
class ModelProfile:
    """Profile of a model's capabilities"""
    model_id: str
    provider: str
    speed_score: float  # 0-1, higher is faster
    quality_score: float  # 0-1, higher is better
    cost_per_1k_tokens: float
    strengths: List[str]
    weaknesses: List[str]
    context_length: int
    supports_reasoning: bool = False


@dataclass
class RoutingDecision:
    """Result of a routing decision"""
    task_type: TaskType
    selected_model: str
    complexity_tier: ComplexityTier
    urgency: UrgencyLevel
    confidence: float  # 0-1
    reasoning: str
    alternatives: List[str]  # Fallback models
    estimated_cost: float
    estimated_time_seconds: int


class ModelRegistry:
    """Registry of available models and their profiles"""
    
    DEFAULT_MODELS = {
        # Fast/cheap models (good for synthesis, quick tasks)
        "google/gemini-2.0-flash": ModelProfile(
            model_id="google/gemini-2.0-flash",
            provider="google",
            speed_score=0.95,
            quality_score=0.75,
            cost_per_1k_tokens=0.00015,
            strengths=["fast_retrieval", "large_context", "factual_lookup"],
            weaknesses=["creative_writing", "nuanced_analysis"],
            context_length=1000000,
            supports_reasoning=False
        ),
        
        "openai/gpt-4o-mini": ModelProfile(
            model_id="openai/gpt-4o-mini",
            provider="openai",
            speed_score=0.90,
            quality_score=0.70,
            cost_per_1k_tokens=0.00015,
            strengths=["fast_processing", "code", "structured_output"],
            weaknesses=["deep_reasoning", "academic_nuance"],
            context_length=128000,
            supports_reasoning=False
        ),
        
        # Balanced models (good middle ground)
        "anthropic/claude-3.5-sonnet": ModelProfile(
            model_id="anthropic/claude-3.5-sonnet",
            provider="anthropic",
            speed_score=0.75,
            quality_score=0.85,
            cost_per_1k_tokens=0.003,
            strengths=["balanced", "good_instructions", "voice_matching"],
            weaknesses=["very_long_context"],
            context_length=200000,
            supports_reasoning=False
        ),
        
        "openai/gpt-4o": ModelProfile(
            model_id="openai/gpt-4o",
            provider="openai",
            speed_score=0.70,
            quality_score=0.88,
            cost_per_1k_tokens=0.0025,
            strengths=["analysis", "review", "critical_thinking", "different_perspective"],
            weaknesses=["very_creative_writing"],
            context_length=128000,
            supports_reasoning=False
        ),
        
        # High quality models (best for difficult tasks)
        "anthropic/claude-opus-4": ModelProfile(
            model_id="anthropic/claude-opus-4",
            provider="anthropic",
            speed_score=0.55,
            quality_score=0.95,
            cost_per_1k_tokens=0.015,
            strengths=["creative_writing", "voice_constrained", "academic", "nuanced"],
            weaknesses=["slow", "expensive"],
            context_length=200000,
            supports_reasoning=True
        ),
        
        "anthropic/claude-opus-4.5": ModelProfile(
            model_id="anthropic/claude-opus-4.5",
            provider="anthropic",
            speed_score=0.52,
            quality_score=0.96,
            cost_per_1k_tokens=0.018,
            strengths=["best_creative", "academic_excellence", "voice_matching", "synthesis"],
            weaknesses=["slowest", "expensive"],
            context_length=200000,
            supports_reasoning=True
        ),
        
        "openai/o3-mini": ModelProfile(
            model_id="openai/o3-mini",
            provider="openai",
            speed_score=0.60,
            quality_score=0.92,
            cost_per_1k_tokens=0.008,
            strengths=["reasoning", "complex_analysis", "structured_thinking"],
            weaknesses=["creative_writing"],
            context_length=200000,
            supports_reasoning=True
        ),
    }
    
    def __init__(self, custom_models: Optional[Dict[str, ModelProfile]] = None):
        self.models = {**self.DEFAULT_MODELS}
        if custom_models:
            self.models.update(custom_models)
    
    def get_model(self, model_id: str) -> Optional[ModelProfile]:
        """Get a model profile by ID"""
        return self.models.get(model_id)
    
    def get_models_for_task(self, task_type: TaskType) -> List[ModelProfile]:
        """Get models suitable for a specific task"""
        task_strengths = {
            TaskType.SYNTHESIS: ["fast_retrieval", "large_context", "factual_lookup"],
            TaskType.DRAFTING: ["creative_writing", "voice_constrained", "academic", "nuanced"],
            TaskType.AUDIT: ["analysis", "review", "critical_thinking", "different_perspective"],
            TaskType.VOICE_EXTRACTION: ["balanced", "voice_matching", "good_instructions"],
            TaskType.VALIDATION: ["analysis", "review", "structured_thinking"],
        }
        
        required_strengths = task_strengths.get(task_type, [])
        suitable = []
        
        for model in self.models.values():
            # Score based on matching strengths
            score = sum(1 for s in required_strengths if s in model.strengths)
            if score > 0 or task_type == TaskType.VALIDATION:
                suitable.append((score, model))
        
        # Sort by score descending
        suitable.sort(key=lambda x: x[0], reverse=True)
        return [m for _, m in suitable]


class ComplexityAnalyzer:
    """Analyzes content to determine complexity tier"""
    
    def analyze(self, content: str, task_type: TaskType) -> ComplexityTier:
        """
        Analyze content complexity based on multiple factors.
        """
        word_count = len(content.split())
        
        # Factor 1: Length
        if word_count > 10000:
            length_score = 3  # Very long
        elif word_count > 5000:
            length_score = 2  # Long
        elif word_count > 1000:
            length_score = 1  # Medium
        else:
            length_score = 0  # Short
        
        # Factor 2: Vocabulary sophistication
        complex_words = len(re.findall(r'\b(theoretical|framework|methodology|epistemology|ontological|heuristic|paradigm|dialectic|hermeneutic|phenomenological)\b', content, re.IGNORECASE))
        vocab_score = min(3, complex_words // 2)
        
        # Factor 3: Citation density (academic complexity)
        citations = len(re.findall(r'\([A-Z][a-z]+.*\d{4}|\d{4}\)', content))
        citation_score = min(3, citations // 5)
        
        # Factor 4: Nuance markers
        nuance_markers = len(re.findall(r'\b(however|although|nevertheless|conversely|paradoxically|tension|contradiction|ambiguity|complexity)\b', content, re.IGNORECASE))
        nuance_score = min(3, nuance_markers // 3)
        
        # Factor 5: Domain-specific terminology
        if task_type == TaskType.SYNTHESIS:
            domain_terms = len(re.findall(r'\b(literature|review|synthesis|prior work|existing research|empirical|quantitative|qualitative|mixed.methods)\b', content, re.IGNORECASE))
        elif task_type == TaskType.DRAFTING:
            domain_terms = len(re.findall(r'\b(argument|claim|evidence|analysis|findings|implications|contribution)\b', content, re.IGNORECASE))
        else:
            domain_terms = 0
        domain_score = min(2, domain_terms // 5)
        
        # Calculate total score
        total_score = length_score + vocab_score + citation_score + nuance_score + domain_score
        
        # Map to complexity tier
        if total_score >= 8:
            return ComplexityTier.EXTREME
        elif total_score >= 5:
            return ComplexityTier.HIGH
        elif total_score >= 2:
            return ComplexityTier.MEDIUM
        else:
            return ComplexityTier.LOW
    
    def get_rationale(self, content: str, tier: ComplexityTier) -> str:
        """Generate human-readable rationale for complexity tier"""
        rationales = {
            ComplexityTier.LOW: "Simple, straightforward content with minimal complexity",
            ComplexityTier.MEDIUM: "Moderate complexity requiring balanced approach",
            ComplexityTier.HIGH: "Complex content with nuanced arguments requiring high-quality model",
            ComplexityTier.EXTREME: "Highly complex content requiring best available model for quality",
        }
        return rationales.get(tier, "Unknown complexity")


class HybridModelRouter:
    """
    Main router class that makes intelligent model selection decisions.
    
    Replaces hardcoded model assignments with dynamic routing based on:
    - Task type
    - Content complexity
    - Urgency requirements
    - Cost considerations
    """
    
    # Default timeout recommendations by model speed
    TIMEOUT_RECOMMENDATIONS = {
        "google/gemini-2.0-flash": 180,
        "openai/gpt-4o-mini": 180,
        "anthropic/claude-3.5-sonnet": 300,
        "openai/gpt-4o": 300,
        "openai/o3-mini": 400,
        "anthropic/claude-opus-4": 600,
        "anthropic/claude-opus-4.5": 600,
    }
    
    def __init__(self, 
                 model_registry: Optional[ModelRegistry] = None,
                 complexity_analyzer: Optional[ComplexityAnalyzer] = None,
                 cost_budget: Optional[float] = None,
                 prefer_reasoning: bool = False):
        self.registry = model_registry or ModelRegistry()
        self.analyzer = complexity_analyzer or ComplexityAnalyzer()
        self.cost_budget = cost_budget
        self.prefer_reasoning = prefer_reasoning
        
        # Routing history for learning
        self.routing_history: List[Dict] = []
    
    def route(self, 
              task_type: TaskType,
              content: str,
              urgency: UrgencyLevel = UrgencyLevel.BALANCED,
              user_preference: Optional[str] = None,
              context: Optional[Dict] = None) -> RoutingDecision:
        """
        Make a routing decision for a task.
        
        Args:
            task_type: Type of task being performed
            content: The content to process
            urgency: Speed vs quality preference
            user_preference: Optional specific model user wants
            context: Additional context (voice_profile, stage, etc.)
        
        Returns:
            RoutingDecision with selected model and reasoning
        """
        context = context or {}
        
        # Analyze complexity
        complexity = self.analyzer.analyze(content, task_type)
        
        # Get suitable models for this task
        suitable_models = self.registry.get_models_for_task(task_type)
        
        # Apply urgency filtering
        if urgency == UrgencyLevel.FAST:
            # Filter to fast models only
            suitable_models = [m for m in suitable_models if m.speed_score >= 0.80]
        elif urgency == UrgencyLevel.QUALITY:
            # Filter to high quality models
            suitable_models = [m for m in suitable_models if m.quality_score >= 0.85]
        
        # Apply complexity filtering
        if complexity == ComplexityTier.EXTREME:
            # Require top quality models
            suitable_models = [m for m in suitable_models if m.quality_score >= 0.90]
        elif complexity == ComplexityTier.HIGH:
            # Prefer quality but allow good mid-tier
            suitable_models = [m for m in suitable_models if m.quality_score >= 0.80]
        
        # Apply reasoning preference
        if self.prefer_reasoning and task_type in [TaskType.AUDIT, TaskType.VALIDATION]:
            suitable_models = [m for m in suitable_models if m.supports_reasoning] + suitable_models
        
        # Apply user preference if valid
        if user_preference and user_preference in self.registry.models:
            selected_model = self.registry.models[user_preference]
            confidence = 0.9
            reasoning = f"User-specified model: {user_preference}"
        elif suitable_models:
            # Score and rank models
            scored_models = self._score_models(suitable_models, task_type, complexity, urgency)
            selected_model = scored_models[0][0]
            confidence = scored_models[0][1]
            reasoning = self._generate_reasoning(selected_model, task_type, complexity, urgency, scored_models)
        else:
            # Fallback to a default
            selected_model = self.registry.models["anthropic/claude-3.5-sonnet"]
            confidence = 0.5
            reasoning = "No suitable models found, using fallback"
        
        # Get alternatives (next 2 best options)
        alternatives = [m.model_id for m, _ in scored_models[1:3]] if 'scored_models' in dir() else []
        
        # Estimate cost and time
        estimated_tokens = len(content.split()) * 1.5  # Rough estimate
        estimated_cost = (estimated_tokens / 1000) * selected_model.cost_per_1k_tokens
        estimated_time = self.TIMEOUT_RECOMMENDATIONS.get(selected_model.model_id, 300)
        
        # Log routing decision
        decision = RoutingDecision(
            task_type=task_type,
            selected_model=selected_model.model_id,
            complexity_tier=complexity,
            urgency=urgency,
            confidence=confidence,
            reasoning=reasoning,
            alternatives=alternatives,
            estimated_cost=estimated_cost,
            estimated_time_seconds=estimated_time
        )
        
        self._log_decision(decision, content)
        
        return decision
    
    def _score_models(self, 
                     models: List[ModelProfile],
                     task_type: TaskType,
                     complexity: ComplexityTier,
                     urgency: UrgencyLevel) -> List[Tuple[ModelProfile, float]]:
        """
        Score each model based on task requirements.
        Returns list of (model, score) sorted by score descending.
        """
        scored = []
        
        for model in models:
            score = 0.0
            
            # Base quality score (0-1)
            score += model.quality_score * 0.4
            
            # Speed consideration
            if urgency == UrgencyLevel.FAST:
                score += model.speed_score * 0.4
            elif urgency == UrgencyLevel.QUALITY:
                score += model.speed_score * 0.1
            else:
                score += model.speed_score * 0.2
            
            # Complexity match
            if complexity == ComplexityTier.EXTREME:
                score += model.quality_score * 0.3  # Extra weight on quality
            elif complexity == ComplexityTier.HIGH:
                score += model.quality_score * 0.2
            
            # Cost consideration (penalty for expensive models)
            cost_penalty = model.cost_per_1k_tokens * 10  # Scale to 0-0.3 range
            score -= min(cost_penalty, 0.3)
            
            scored.append((model, max(0, score)))
        
        # Sort by score descending
        scored.sort(key=lambda x: x[1], reverse=True)
        return scored
    
    def _generate_reasoning(self,
                           selected: ModelProfile,
                           task_type: TaskType,
                           complexity: ComplexityTier,
                           urgency: UrgencyLevel,
                           scored_models: List[Tuple[ModelProfile, float]]) -> str:
        """Generate human-readable reasoning for the selection"""
        reasons = []
        
        reasons.append(f"Selected {selected.model_id} for {task_type.value}")
        reasons.append(f"Content complexity: {complexity.value}")
        reasons.append(f"Urgency preference: {urgency.value}")
        
        if urgency == UrgencyLevel.FAST:
            reasons.append(f"Prioritized speed (score: {selected.speed_score:.2f})")
        elif urgency == UrgencyLevel.QUALITY:
            reasons.append(f"Prioritized quality (score: {selected.quality_score:.2f})")
        
        if complexity in [ComplexityTier.HIGH, ComplexityTier.EXTREME]:
            reasons.append(f"High complexity requires quality model")
        
        # Mention alternatives
        if len(scored_models) > 1:
            alt = scored_models[1][0]
            reasons.append(f"Alternative: {alt.model_id} (score: {scored_models[1][1]:.2f})")
        
        return "; ".join(reasons)
    
    def _log_decision(self, decision: RoutingDecision, content: str):
        """Log routing decision for future analysis"""
        entry = {
            "timestamp": datetime.now().isoformat(),
            "decision": asdict(decision),
            "content_hash": hashlib.md5(content.encode()).hexdigest()[:16],
        }
        self.routing_history.append(entry)
    
    def get_recommended_config(self, decision: RoutingDecision) -> Dict:
        """
        Get OpenClaw sessions_spawn configuration for a routing decision.
        """
        model = decision.selected_model
        timeout = self.TIMEOUT_RECOMMENDATIONS.get(model, 300)
        
        return {
            "model": model,
            "runTimeoutSeconds": timeout,
            "strategy": "hybrid_routed",
            "routing": {
                "task_type": decision.task_type.value,
                "complexity": decision.complexity_tier.value,
                "urgency": decision.urgency.value,
                "confidence": decision.confidence,
                "reasoning": decision.reasoning,
            }
        }
    
    def get_model_for_stage(self, 
                           stage: str,
                           content: str = "",
                           urgency: UrgencyLevel = UrgencyLevel.BALANCED) -> RoutingDecision:
        """
        Convenience method for getting model by pipeline stage.
        
        Stages: concept_validation, synthesis, voice_learning, 
                drafting, audit, revision
        """
        stage_map = {
            "concept_validation": TaskType.VALIDATION,
            "synthesis": TaskType.SYNTHESIS,
            "voice_learning": TaskType.VOICE_EXTRACTION,
            "drafting": TaskType.DRAFTING,
            "audit": TaskType.AUDIT,
            "revision": TaskType.DRAFTING,
        }
        
        task_type = stage_map.get(stage, TaskType.DRAFTING)
        return self.route(task_type, content, urgency)


# Legacy compatibility: Static model assignments for backwards compatibility
# These are replaced by dynamic routing but kept for reference
LEGACY_MODEL_ASSIGNMENTS = {
    TaskType.SYNTHESIS: "google/gemini-2.0-flash",
    TaskType.DRAFTING: "anthropic/claude-opus-4.5",
    TaskType.AUDIT: "openai/gpt-4o",
    TaskType.VOICE_EXTRACTION: "anthropic/claude-3.5-sonnet",
    TaskType.VALIDATION: "openai/gpt-4o",
}


def create_router(cost_budget: Optional[float] = None,
                  prefer_reasoning: bool = False) -> HybridModelRouter:
    """
    Factory function to create a configured router instance.
    
    Usage:
        router = create_router(cost_budget=1.0, prefer_reasoning=True)
        decision = router.route(TaskType.DRAFTING, content, UrgencyLevel.QUALITY)
        config = router.get_recommended_config(decision)
    """
    return HybridModelRouter(
        cost_budget=cost_budget,
        prefer_reasoning=prefer_reasoning
    )


# Example usage
if __name__ == "__main__":
    # Test the router
    router = create_router(prefer_reasoning=True)
    
    # Test content
    test_content = """
    Research Question: How do algorithmic curation systems shape public discourse
    on climate change? Drawing on Bennett and Pfetsch (2018) and Boczkowski (2010),
    I examine the tension between platform logics and democratic ideals.
    """
    
    print("Testing Hybrid Model Router...\n")
    
    # Test different task types
    for task in [TaskType.SYNTHESIS, TaskType.DRAFTING, TaskType.AUDIT]:
        for urgency in [UrgencyLevel.FAST, UrgencyLevel.BALANCED, UrgencyLevel.QUALITY]:
            decision = router.route(task, test_content, urgency)
            print(f"\n{task.value.upper()} | {urgency.value}")
            print(f"  Selected: {decision.selected_model}")
            print(f"  Confidence: {decision.confidence:.2f}")
            print(f"  ETA: {decision.estimated_time_seconds}s")
            print(f"  Complexity: {decision.complexity_tier.value}")
    
    print("\n\nRecommended configs:")
    for stage in ["synthesis", "drafting", "audit"]:
        decision = router.get_model_for_stage(stage, test_content)
        config = router.get_recommended_config(decision)
        print(f"\n{stage}: {config['model']} (timeout: {config['runTimeoutSeconds']}s)")
