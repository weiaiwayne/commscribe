"""
Enhanced Research Pipeline with Guardrails and Multi-Draft Support
"""

import re
import json
from pathlib import Path
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class ConceptAssessment:
    """Assessment of concept plan quality"""
    has_research_question: bool
    has_theoretical_framing: bool
    has_literature_grounding: bool
    has_original_voice: bool
    word_count: int
    citation_count: int
    depth_score: float  # 0-1
    recommendation: str
    feedback: List[str]
    can_proceed: bool


@dataclass
class DraftVersion:
    """Track a draft version"""
    version: int
    content: str
    submitted_at: str
    agent_comments: List[Dict]
    user_revisions: str
    status: str  # 'submitted', 'reviewed', 'revised', 'final'


@dataclass
class ProjectState:
    """Full project state tracking"""
    project_id: str
    user_id: str
    topic: str
    current_stage: str
    concept_assessment: Optional[ConceptAssessment]
    draft_history: List[DraftVersion]
    max_drafts_allowed: int
    created_at: str
    last_updated: str


class ConceptValidator:
    """
    Validates concept plans to prevent lazy shortcuts.
    Ensures nuance, original voice, and literature grounding.
    """
    
    MIN_WORD_COUNT = 300  # Minimum for a nuanced concept
    MIN_CITATIONS = 3     # Minimum literature references
    
    def __init__(self):
        self.generic_phrases = [
            r'\bthis paper will explore\b',
            r'\bthis study aims to\b',
            r'\bit is important to understand\b',
            r'\bin recent years\b',
            r'\bwith the rise of\b',
            r'\bthe purpose of this research is to\b',
        ]
        
        self.depth_indicators = [
            r'\bhowever\b|\bbut\b|\byet\b|\balthough\b',  # Nuance markers
            r'\bgap\b|\blimitation\b|\bcritique\b',  # Critical thinking
            r'\baccording to\b|\bargues\b|\bsuggests\b|\bcontends\b',  # Engagement
            r'\btheoretical\b|\bframework\b|\blens\b|\bperspective\b',  # Theory
            r'\bmethod\b|\bapproach\b|\banalysis\b|\bdata\b',  # Methodology
        ]
    
    def assess(self, concept_text: str) -> ConceptAssessment:
        """
        Comprehensive assessment of concept plan quality.
        Returns assessment with recommendation on whether to proceed.
        """
        word_count = len(concept_text.split())
        
        # Check for research question
        has_rq = self._has_research_question(concept_text)
        
        # Check for theoretical framing
        has_theory = self._has_theoretical_framing(concept_text)
        
        # Check literature grounding
        citations = self._extract_citations(concept_text)
        has_grounding = len(citations) >= self.MIN_CITATIONS
        
        # Check for original voice (not generic)
        has_voice = self._has_original_voice(concept_text)
        
        # Calculate depth score
        depth_score = self._calculate_depth(concept_text)
        
        # Generate feedback
        feedback = self._generate_feedback(
            word_count, has_rq, has_theory, has_grounding, 
            has_voice, len(citations), concept_text
        )
        
        # Determine if can proceed
        can_proceed = (
            word_count >= self.MIN_WORD_COUNT and
            has_rq and
            has_grounding and
            depth_score >= 0.4
        )
        
        recommendation = (
            "PROCEED" if can_proceed 
            else "REVISE - Address feedback before continuing"
        )
        
        return ConceptAssessment(
            has_research_question=has_rq,
            has_theoretical_framing=has_theory,
            has_literature_grounding=has_grounding,
            has_original_voice=has_voice,
            word_count=word_count,
            citation_count=len(citations),
            depth_score=depth_score,
            recommendation=recommendation,
            feedback=feedback,
            can_proceed=can_proceed
        )
    
    def _has_research_question(self, text: str) -> bool:
        """Detect explicit research question(s)"""
        patterns = [
            r'\b(research question|rq|r\.q\.|research q)\b',
            r'\bthis (paper|study|research) asks\b',
            r'\b(i|we) ask\b.*\b(whether|how|why|what)\b',
            r'\b(i|we) (seek to|aim to|want to) (understand|explore|investigate)\b',
            r'\?.*\?',  # Multiple questions suggest inquiry
        ]
        return any(re.search(p, text, re.IGNORECASE) for p in patterns)
    
    def _has_theoretical_framing(self, text: str) -> bool:
        """Check for theoretical framework or lens"""
        patterns = [
            r'\b(theoretical framework|conceptual framework|theoretical lens)\b',
            r'\b(grounded in|informed by|drawing on)\b.*\b(theory|literature|scholarship)\b',
            r'\b(i|we) (use|employ|adopt|apply)\b.*\b(theory|approach|perspective)\b',
            r'\b(sociological|political|communication|psychological)\b.*\b(theory|perspective)\b',
        ]
        return any(re.search(p, text, re.IGNORECASE) for p in patterns)
    
    def _extract_citations(self, text: str) -> List[str]:
        """Extract academic citations"""
        # APA style: Author (Year) or (Author, Year)
        apa_pattern = r'\b([A-Z][a-z]+(?:\s+and\s+[A-Z][a-z]+)?\s+\(\d{4}[a-z]?\))'
        # Parenthetical citations
        paren_pattern = r'\(([A-Z][a-z]+(?:\s+et\s+al\.)?(?:,\s+\d{4}[a-z]?)+)\)'
        
        citations = []
        citations.extend(re.findall(apa_pattern, text))
        citations.extend(re.findall(paren_pattern, text))
        return citations
    
    def _has_original_voice(self, text: str) -> bool:
        """Check for original voice vs generic AI language"""
        generic_count = sum(1 for p in self.generic_phrases if re.search(p, text, re.IGNORECASE))
        
        # Personal pronouns suggest authorial voice
        personal_markers = len(re.findall(r'\b(i|my|myself|we|our)\b', text, re.IGNORECASE))
        
        # Specific details suggest grounded knowledge
        specific_details = len(re.findall(r'\b\d{4}\b|\b(?:study|paper|article|book)\s+(?:by|from|in)\b', text, re.IGNORECASE))
        
        # Score: low generic phrases + personal markers + specific details = original voice
        score = (personal_markers * 0.3) + (specific_details * 0.5) - (generic_count * 0.5)
        return score > 2.0
    
    def _calculate_depth(self, text: str) -> float:
        """Calculate conceptual depth score 0-1"""
        word_count = len(text.split())
        if word_count < 100:
            return 0.0
        
        depth_matches = sum(len(re.findall(p, text, re.IGNORECASE)) for p in self.depth_indicators)
        
        # Normalize by word count (expect ~1 depth marker per 50 words for good depth)
        expected_markers = word_count / 50
        depth_score = min(1.0, depth_matches / expected_markers)
        
        return depth_score
    
    def _generate_feedback(self, word_count: int, has_rq: bool, has_theory: bool,
                          has_grounding: bool, has_voice: bool, citation_count: int,
                          text: str) -> List[str]:
        """Generate specific improvement feedback"""
        feedback = []
        
        if word_count < self.MIN_WORD_COUNT:
            feedback.append(f"⚠️ Concept plan is too brief ({word_count} words). Aim for at least {self.MIN_WORD_COUNT} words to demonstrate sufficient depth.")
        
        if not has_rq:
            feedback.append("❌ No clear research question detected. Explicitly state what you aim to understand or investigate.")
        
        if not has_grounding:
            feedback.append(f"❌ Insufficient literature grounding ({citation_count} citations). Reference at least {self.MIN_CITATIONS} key works to show you know the field.")
        
        if not has_theory:
            feedback.append("⚠️ No theoretical framework identified. What lens or perspective will guide your analysis?")
        
        if not has_voice:
            feedback.append("⚠️ Writing appears generic. Use more personal pronouns (I/we/my) and specific details from your reading to establish your authorial voice.")
        
        # Check for contradictions or tensions (good sign)
        if not re.search(r'\b(however|yet|although|tension|contradiction|debate)\b', text, re.IGNORECASE):
            feedback.append("💡 Consider identifying a tension, debate, or gap in existing literature that your review will address.")
        
        if len(feedback) == 0:
            feedback.append("✅ Strong concept plan with clear research question, theoretical framing, and literature grounding.")
        
        return feedback


class DraftStateDetector:
    """
    Detects whether input is rough concept, draft in progress, or polished paper.
    Routes to appropriate workflow stage.
    """
    
    def detect(self, text: str, user_context: str = "") -> Dict:
        """
        Analyze text to determine its stage and characteristics.
        Returns routing recommendation.
        """
        word_count = len(text.split())
        
        # Check for section headers (indicates structured draft)
        has_sections = bool(re.search(r'\n#{1,3}\s+\w+|\n\d+\.\s+\w+|\n[A-Z][A-Z\s]{3,}\n', text))
        
        # Check for citations (indicates literature engagement)
        citation_count = len(re.findall(r'\([A-Z][a-z]+.*\d{4}|\d{4}\)', text))
        
        # Check for conclusion/synthesis (indicates mature draft)
        has_conclusion = bool(re.search(r'\b(conclusion|concluding|synthesis|synthesizing|in sum|to conclude)\b', text, re.IGNORECASE))
        
        # Check for references section
        has_references = bool(re.search(r'\n#*\s*references|bibliography', text, re.IGNORECASE))
        
        # Check for polish indicators
        polish_indicators = [
            r'\b(furthermore|moreover|consequently|nevertheless)\b',
            r'\b(this (paper|review|study) (argues|demonstrates|shows|contends))\b',
            r'\b(firstly|secondly|thirdly|finally)\b',
        ]
        polish_score = sum(1 for p in polish_indicators if re.search(p, text, re.IGNORECASE))
        
        # Determine stage
        if word_count < 400 and not has_sections and citation_count < 3:
            stage = "concept_plan"
            description = "Early concept plan - needs validation before proceeding"
            recommended_action = "Run concept validation"
        
        elif has_sections and word_count > 1000 and citation_count > 5 and not has_conclusion:
            stage = "partial_draft"
            description = "Draft in progress (~50-70% complete)"
            recommended_action = "Continue drafting with synthesis support"
        
        elif has_sections and has_conclusion and citation_count > 10:
            stage = "mature_draft"
            description = "Well-developed draft (~80%+ complete)"
            recommended_action = "Critical review and refinement"
        
        elif has_references and polish_score >= 2:
            stage = "polished_paper"
            description = "Near-final paper needing minor refinement"
            recommended_action = "Final audit and polish"
        
        else:
            stage = "ambiguous"
            description = "Unclear stage - needs clarification"
            recommended_action = "Ask user for context"
        
        return {
            "detected_stage": stage,
            "description": description,
            "recommended_action": recommended_action,
            "metrics": {
                "word_count": word_count,
                "has_sections": has_sections,
                "citation_count": citation_count,
                "has_conclusion": has_conclusion,
                "has_references": has_references,
                "polish_score": polish_score
            }
        }


class MultiDraftWorkflow:
    """
    Manages iterative draft refinement with version control.
    """
    
    MAX_DRAFTS = 5  # Maximum iterations
    
    def __init__(self, project_dir: str = "~/clawd/research/projects"):
        self.project_dir = Path(project_dir).expanduser()
        self.project_dir.mkdir(parents=True, exist_ok=True)
        self.validator = ConceptValidator()
        self.detector = DraftStateDetector()
    
    def start_project(self, user_id: str, topic: str, initial_input: str) -> Dict:
        """
        Initialize a new research project.
        Validates concept plan before allowing progression.
        """
        project_id = f"{user_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        # Detect what stage the input is at
        detection = self.detector.detect(initial_input)
        
        # If it's a concept plan, validate it
        if detection["detected_stage"] == "concept_plan":
            assessment = self.validator.assess(initial_input)
            
            if not assessment.can_proceed:
                return {
                    "status": "VALIDATION_FAILED",
                    "project_id": project_id,
                    "assessment": asdict(assessment),
                    "message": "Concept plan needs revision before proceeding.",
                    "next_action": "Address the feedback and resubmit."
                }
            
            # Create project with validated concept
            state = ProjectState(
                project_id=project_id,
                user_id=user_id,
                topic=topic,
                current_stage="concept_validated",
                concept_assessment=assessment,
                draft_history=[],
                max_drafts_allowed=self.MAX_DRAFTS,
                created_at=datetime.now().isoformat(),
                last_updated=datetime.now().isoformat()
            )
            
            self._save_state(state)
            
            return {
                "status": "CONCEPT_VALIDATED",
                "project_id": project_id,
                "assessment": asdict(assessment),
                "message": "Concept plan approved. Ready to proceed to Stage 2 (literature synthesis).",
                "next_action": "Run literature search and synthesis"
            }
        
        # If it's already a draft, assess and route appropriately
        else:
            state = ProjectState(
                project_id=project_id,
                user_id=user_id,
                topic=topic,
                current_stage=detection["detected_stage"],
                concept_assessment=None,
                draft_history=[],
                max_drafts_allowed=self.MAX_DRAFTS,
                created_at=datetime.now().isoformat(),
                last_updated=datetime.now().isoformat()
            )
            
            self._save_state(state)
            
            return {
                "status": "DRAFT_DETECTED",
                "project_id": project_id,
                "detection": detection,
                "message": f"Detected {detection['description']}",
                "next_action": detection["recommended_action"]
            }
    
    def submit_draft(self, project_id: str, draft_content: str, 
                     user_notes: str = "") -> Dict:
        """
        Submit a draft for agent review.
        Tracks version history.
        """
        state = self._load_state(project_id)
        
        if not state:
            return {"error": "Project not found"}
        
        if len(state.draft_history) >= state.max_drafts_allowed:
            return {
                "status": "MAX_DRAFTS_REACHED",
                "message": f"Maximum {state.max_drafts_allowed} drafts allowed. Final version should be ready.",
                "draft_count": len(state.draft_history)
            }
        
        # Detect what stage this draft is at
        detection = self.detector.detect(draft_content, user_notes)
        
        # Create new draft version
        new_version = DraftVersion(
            version=len(state.draft_history) + 1,
            content=draft_content,
            submitted_at=datetime.now().isoformat(),
            agent_comments=[],  # Will be populated by review agent
            user_revisions=user_notes,
            status='submitted'
        )
        
        state.draft_history.append(new_version)
        state.current_stage = f"draft_v{new_version.version}_submitted"
        state.last_updated = datetime.now().isoformat()
        
        self._save_state(state)
        
        return {
            "status": "DRAFT_SUBMITTED",
            "project_id": project_id,
            "version": new_version.version,
            "detection": detection,
            "message": f"Draft v{new_version.version} submitted for review",
            "next_action": "Wait for agent review or trigger review now"
        }
    
    def add_agent_review(self, project_id: str, version: int, 
                         comments: List[Dict]) -> Dict:
        """
        Add agent comments to a specific draft version.
        """
        state = self._load_state(project_id)
        
        if not state or version > len(state.draft_history):
            return {"error": "Draft version not found"}
        
        draft = state.draft_history[version - 1]
        draft.agent_comments = comments
        draft.status = 'reviewed'
        
        state.current_stage = f"draft_v{version}_reviewed"
        state.last_updated = datetime.now().isoformat()
        
        self._save_state(state)
        
        return {
            "status": "REVIEW_ADDED",
            "project_id": project_id,
            "version": version,
            "comment_count": len(comments),
            "message": f"Agent review added to Draft v{version}",
            "next_action": "User should revise based on comments and submit next draft"
        }
    
    def get_project_status(self, project_id: str) -> Dict:
        """Get full project status and history"""
        state = self._load_state(project_id)
        
        if not state:
            return {"error": "Project not found"}
        
        return {
            "project_id": state.project_id,
            "topic": state.topic,
            "current_stage": state.current_stage,
            "concept_assessment": asdict(state.concept_assessment) if state.concept_assessment else None,
            "draft_history": [
                {
                    "version": d.version,
                    "submitted_at": d.submitted_at,
                    "status": d.status,
                    "comment_count": len(d.agent_comments),
                    "word_count": len(d.content.split()) if d.content else 0
                }
                for d in state.draft_history
            ],
            "drafts_remaining": state.max_drafts_allowed - len(state.draft_history),
            "created_at": state.created_at,
            "last_updated": state.last_updated
        }
    
    def _save_state(self, state: ProjectState):
        """Save project state to file"""
        filepath = self.project_dir / f"{state.project_id}.json"
        with open(filepath, 'w') as f:
            json.dump(asdict(state), f, indent=2, default=str)
    
    def _load_state(self, project_id: str) -> Optional[ProjectState]:
        """Load project state from file"""
        filepath = self.project_dir / f"{project_id}.json"
        if not filepath.exists():
            return None
        
        with open(filepath, 'r') as f:
            data = json.load(f)
        
        # Reconstruct draft history
        draft_history = [DraftVersion(**d) for d in data.get('draft_history', [])]
        
        # Reconstruct concept assessment
        concept = None
        if data.get('concept_assessment'):
            concept = ConceptAssessment(**data['concept_assessment'])
        
        return ProjectState(
            project_id=data['project_id'],
            user_id=data['user_id'],
            topic=data['topic'],
            current_stage=data['current_stage'],
            concept_assessment=concept,
            draft_history=draft_history,
            max_drafts_allowed=data['max_drafts_allowed'],
            created_at=data['created_at'],
            last_updated=data['last_updated']
        )


# Convenience function for integration
def process_research_submission(user_id: str, topic: str, content: str,
                                project_id: Optional[str] = None) -> Dict:
    """
    Main entry point for processing research submissions.
    Handles both new projects and draft revisions.
    """
    workflow = MultiDraftWorkflow()
    
    # If no project_id, start new project
    if not project_id:
        return workflow.start_project(user_id, topic, content)
    
    # Otherwise, submit as draft revision
    return workflow.submit_draft(project_id, content)


if __name__ == "__main__":
    # Test the system
    print("Testing Concept Validator...")
    
    # Test 1: Weak concept (should fail)
    weak_concept = """
    This paper will explore social media and politics. It is important to understand 
    how social media affects political opinions. With the rise of platforms like Twitter 
    and Facebook, this topic is increasingly relevant. This study aims to investigate 
    the relationship between social media use and political engagement.
    """
    
    validator = ConceptValidator()
    assessment = validator.assess(weak_concept)
    print(f"\nWeak Concept Assessment:")
    print(f"Can proceed: {assessment.can_proceed}")
    print(f"Feedback: {assessment.feedback}")
    
    # Test 2: Strong concept (should pass)
    strong_concept = """
    Research Question: How do algorithmic curation systems on social media platforms 
    shape the visibility of climate change content, and what are the implications for 
    public understanding of scientific consensus?
    
    Drawing on Bennett and Pfetsch's (2018) concept of "disinformation order" and 
    Boczkowski's (2010) work on homophily in news consumption, I propose to examine 
    the tension between platform logics of engagement-maximization and democratic 
    ideals of informed citizenship. Existing literature on filter bubbles (Pariser, 2011) 
    and echo chambers (Sunstein, 2017) provides a starting point, but I argue these 
    frameworks insufficiently account for the role of algorithmic intermediaries in 
    constructing what I term "calculated publics"—audiences rendered visible through 
    platform metrics and optimization.
    
    My approach combines network analysis of content diffusion patterns with qualitative 
    analysis of user interpretations. However, I'm uncertain whether to prioritize 
    cross-platform comparison (Twitter vs. TikTok vs. Instagram) or depth within a 
    single platform. The literature on comparative platform studies (Plantin et al., 2018) 
    suggests infrastructure differences matter significantly, yet single-platform studies 
    like those by Vosoughi et al. (2018) on Twitter offer valuable granularity.
    
    I aim to contribute to communication theory by bridging political communication's 
    focus on information quality with platform studies' attention to materiality. 
    A potential gap I see is the lack of longitudinal work tracking how algorithmic 
    changes (e.g., Twitter's shift from chronological to algorithmic feeds) affect 
    climate discourse over time.
    """
    
    assessment2 = validator.assess(strong_concept)
    print(f"\n\nStrong Concept Assessment:")
    print(f"Can proceed: {assessment2.can_proceed}")
    print(f"Word count: {assessment2.word_count}")
    print(f"Citations: {assessment2.citation_count}")
    print(f"Depth score: {assessment2.depth_score:.2f}")
    print(f"Feedback: {assessment2.feedback}")
    
    print("\n\nTesting Draft State Detector...")
    detector = DraftStateDetector()
    
    detection1 = detector.detect(weak_concept)
    print(f"\nWeak concept detected as: {detection1['detected_stage']}")
    
    detection2 = detector.detect(strong_concept)
    print(f"Strong concept detected as: {detection2['detected_stage']}")
