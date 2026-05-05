"""
CommScribe Scripts Package

Core modules:
- file_parser: Extract text from .docx, .pdf, .txt, .doc, .rtf
- voice_learning: Statistical voice extraction
- adaptive_voice: AI-native voice learning with feedback
- anti_ai_patterns: Pattern detection and avoidance
- validation: Concept and draft validation gates
- model_router: Hybrid model routing (v0.3.0)
- enhanced_pipeline_guardrails: Multi-draft workflow with validation
"""

from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPTS_DIR.parent

# File parsing
from .file_parser import parse_file, parse_files, check_dependencies

# Hybrid Model Router (v0.3.0)
from .model_router import (
    HybridModelRouter,
    ModelRegistry,
    ComplexityAnalyzer,
    TaskType,
    ComplexityTier,
    UrgencyLevel,
    RoutingDecision,
    ModelProfile,
    LEGACY_MODEL_ASSIGNMENTS,
    create_router,
)

__all__ = [
    # File parsing
    "parse_file", "parse_files", "check_dependencies",
    # Model router
    "HybridModelRouter", "ModelRegistry", "ComplexityAnalyzer",
    "TaskType", "ComplexityTier", "UrgencyLevel",
    "RoutingDecision", "ModelProfile",
    "LEGACY_MODEL_ASSIGNMENTS", "create_router",
    # Path constants
    "SCRIPTS_DIR", "PROJECT_ROOT",
]
