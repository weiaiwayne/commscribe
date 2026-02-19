"""
CommScribe Scripts Package

Core modules:
- file_parser: Extract text from .docx, .pdf, .txt, .doc, .rtf
- voice_learning: Statistical voice extraction
- adaptive_voice: AI-native voice learning with feedback
- anti_ai_patterns: Pattern detection and avoidance
- validation: Concept and draft validation gates
"""

from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent
PROJECT_ROOT = SCRIPTS_DIR.parent

# File parsing
from .file_parser import parse_file, parse_files, check_dependencies
