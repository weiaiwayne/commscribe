#!/usr/bin/env python3
"""
Adaptive Voice Learning Module for CommScribe

AI-native voice learning that:
1. Uses embeddings to capture style holistically
2. Learns continuously from user feedback
3. Compares new writing against voice signature
4. Adapts profile based on what "sounds like me"

Key difference from statistical extraction:
- Statistical = counts words, measures averages
- Adaptive = learns the gestalt, improves with feedback
"""

import json
import hashlib
import numpy as np
from pathlib import Path
from typing import List, Dict, Optional, Tuple, Any
from dataclasses import dataclass, field, asdict
from datetime import datetime
from abc import ABC, abstractmethod


# ============================================================================
# EMBEDDING PROVIDERS (pluggable)
# ============================================================================

class EmbeddingProvider(ABC):
    """Abstract base for embedding providers"""
    
    @abstractmethod
    def embed(self, texts: List[str]) -> np.ndarray:
        """Return embeddings for texts. Shape: (n_texts, embed_dim)"""
        pass
    
    @property
    @abstractmethod
    def dimension(self) -> int:
        """Embedding dimension"""
        pass


class OpenAIEmbedding(EmbeddingProvider):
    """OpenAI text-embedding-3-small (fast, cheap, good)"""
    
    def __init__(self, api_key: str = None):
        import os
        self.api_key = api_key or os.getenv("OPENAI_API_KEY")
        self._dim = 1536
    
    def embed(self, texts: List[str]) -> np.ndarray:
        import openai
        client = openai.OpenAI(api_key=self.api_key)
        response = client.embeddings.create(
            model="text-embedding-3-small",
            input=texts
        )
        return np.array([e.embedding for e in response.data])
    
    @property
    def dimension(self) -> int:
        return self._dim


class LocalEmbedding(EmbeddingProvider):
    """Local sentence-transformers (no API needed)"""
    
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(model_name)
        self._dim = self.model.get_sentence_embedding_dimension()
    
    def embed(self, texts: List[str]) -> np.ndarray:
        return self.model.encode(texts, convert_to_numpy=True)
    
    @property
    def dimension(self) -> int:
        return self._dim


class OllamaEmbedding(EmbeddingProvider):
    """Ollama local embeddings (nomic-embed-text)"""
    
    def __init__(self, model: str = "nomic-embed-text", host: str = "http://localhost:11434"):
        self.model = model
        self.host = host
        self._dim = 768  # nomic-embed-text dimension
    
    def embed(self, texts: List[str]) -> np.ndarray:
        import requests
        embeddings = []
        for text in texts:
            response = requests.post(
                f"{self.host}/api/embeddings",
                json={"model": self.model, "prompt": text}
            )
            embeddings.append(response.json()["embedding"])
        return np.array(embeddings)
    
    @property
    def dimension(self) -> int:
        return self._dim


# ============================================================================
# VOICE SIGNATURE (the learned representation)
# ============================================================================

@dataclass
class VoiceSignature:
    """
    A learned voice signature that captures writing style holistically.
    
    Unlike statistical profiles that count words, this is a dense vector
    representation that captures the "feel" of writing.
    """
    user_id: str
    created_at: str
    updated_at: str
    
    # Core signature (mean embedding of all samples)
    signature_vector: List[float]
    signature_dim: int
    
    # Sample tracking
    sample_count: int
    sample_hashes: List[str]  # Track which samples we've seen
    total_words: int
    
    # Learned boundaries (updated via feedback)
    similarity_threshold: float  # Below this = "doesn't sound like me"
    confidence: float  # How confident we are in the signature
    
    # Feedback history
    positive_feedback: int = 0  # "sounds like me"
    negative_feedback: int = 0  # "doesn't sound like me"
    
    # Contrastive anchors (what makes this voice distinct)
    contrast_vectors: List[List[float]] = field(default_factory=list)
    contrast_labels: List[str] = field(default_factory=list)  # e.g., "generic_academic", "ai_generated"
    
    def to_numpy(self) -> np.ndarray:
        return np.array(self.signature_vector)
    
    def save(self, path: Path) -> None:
        with open(path, 'w') as f:
            json.dump(asdict(self), f, indent=2)
    
    @classmethod
    def load(cls, path: Path) -> 'VoiceSignature':
        with open(path, 'r') as f:
            data = json.load(f)
        return cls(**data)


# ============================================================================
# ADAPTIVE VOICE LEARNER
# ============================================================================

class AdaptiveVoiceLearner:
    """
    AI-native voice learning that improves with use.
    
    Key features:
    1. Embedding-based - captures holistic style, not just word counts
    2. Continuous learning - improves as it sees more samples
    3. Feedback-driven - learns from "sounds like me" / "doesn't"
    4. Contrastive - learns what makes YOUR voice distinct
    """
    
    def __init__(self, embedding_provider: EmbeddingProvider = None):
        self.embedder = embedding_provider or self._get_default_embedder()
        self.signature: Optional[VoiceSignature] = None
        self._samples: List[str] = []
        self._embeddings: Optional[np.ndarray] = None
    
    def _get_default_embedder(self) -> EmbeddingProvider:
        """Try providers in order of preference"""
        # Try Ollama first (local, free)
        try:
            import requests
            requests.get("http://localhost:11434/api/tags", timeout=1)
            return OllamaEmbedding()
        except:
            pass
        
        # Try sentence-transformers (local, free)
        try:
            return LocalEmbedding()
        except ImportError:
            pass
        
        # Fall back to OpenAI
        import os
        if os.getenv("OPENAI_API_KEY"):
            return OpenAIEmbedding()
        
        raise RuntimeError(
            "No embedding provider available. Install sentence-transformers, "
            "run Ollama, or set OPENAI_API_KEY"
        )
    
    def _hash_text(self, text: str) -> str:
        """Create hash to track seen samples"""
        return hashlib.sha256(text.encode()).hexdigest()[:16]
    
    def _chunk_text(self, text: str, chunk_size: int = 500) -> List[str]:
        """Split text into chunks for more granular embeddings"""
        words = text.split()
        chunks = []
        for i in range(0, len(words), chunk_size):
            chunk = ' '.join(words[i:i + chunk_size])
            if len(chunk.split()) >= 100:  # Minimum viable chunk
                chunks.append(chunk)
        return chunks if chunks else [text]
    
    # -------------------------------------------------------------------------
    # LEARNING
    # -------------------------------------------------------------------------
    
    def learn_from_samples(self, 
                           texts: List[str], 
                           user_id: str,
                           existing_signature: VoiceSignature = None) -> VoiceSignature:
        """
        Learn voice signature from writing samples.
        
        If existing_signature provided, updates it rather than starting fresh.
        """
        # Chunk texts for granular embeddings
        all_chunks = []
        chunk_sources = []
        for i, text in enumerate(texts):
            chunks = self._chunk_text(text)
            all_chunks.extend(chunks)
            chunk_sources.extend([i] * len(chunks))
        
        # Generate embeddings
        print(f"Embedding {len(all_chunks)} chunks from {len(texts)} samples...")
        embeddings = self.embedder.embed(all_chunks)
        
        # Calculate signature (weighted mean)
        signature_vector = np.mean(embeddings, axis=0)
        
        # Calculate initial similarity threshold
        similarities = self._cosine_similarity(embeddings, signature_vector)
        threshold = float(np.percentile(similarities, 10))  # 10th percentile
        
        # Track samples
        sample_hashes = [self._hash_text(t) for t in texts]
        total_words = sum(len(t.split()) for t in texts)
        
        if existing_signature:
            # Incremental update
            old_weight = existing_signature.sample_count
            new_weight = len(texts)
            total_weight = old_weight + new_weight
            
            # Weighted average of signatures
            old_vec = np.array(existing_signature.signature_vector)
            new_vec = signature_vector
            combined = (old_vec * old_weight + new_vec * new_weight) / total_weight
            
            self.signature = VoiceSignature(
                user_id=user_id,
                created_at=existing_signature.created_at,
                updated_at=datetime.now().isoformat(),
                signature_vector=combined.tolist(),
                signature_dim=self.embedder.dimension,
                sample_count=total_weight,
                sample_hashes=list(set(existing_signature.sample_hashes + sample_hashes)),
                total_words=existing_signature.total_words + total_words,
                similarity_threshold=min(threshold, existing_signature.similarity_threshold),
                confidence=min(0.95, existing_signature.confidence + 0.05 * len(texts)),
                positive_feedback=existing_signature.positive_feedback,
                negative_feedback=existing_signature.negative_feedback,
                contrast_vectors=existing_signature.contrast_vectors,
                contrast_labels=existing_signature.contrast_labels,
            )
        else:
            # Fresh signature
            self.signature = VoiceSignature(
                user_id=user_id,
                created_at=datetime.now().isoformat(),
                updated_at=datetime.now().isoformat(),
                signature_vector=signature_vector.tolist(),
                signature_dim=self.embedder.dimension,
                sample_count=len(texts),
                sample_hashes=sample_hashes,
                total_words=total_words,
                similarity_threshold=threshold,
                confidence=min(0.9, 0.3 + 0.1 * len(texts)),  # More samples = more confidence
                positive_feedback=0,
                negative_feedback=0,
            )
        
        self._samples = texts
        self._embeddings = embeddings
        
        return self.signature
    
    def add_contrast(self, 
                     texts: List[str], 
                     label: str) -> None:
        """
        Add contrastive examples (what this voice is NOT).
        
        e.g., add_contrast(ai_generated_samples, "ai_generated")
        """
        if not self.signature:
            raise ValueError("Learn from samples first")
        
        # Embed contrast samples
        all_chunks = []
        for text in texts:
            all_chunks.extend(self._chunk_text(text))
        
        embeddings = self.embedder.embed(all_chunks)
        contrast_vector = np.mean(embeddings, axis=0)
        
        self.signature.contrast_vectors.append(contrast_vector.tolist())
        self.signature.contrast_labels.append(label)
        self.signature.updated_at = datetime.now().isoformat()
    
    # -------------------------------------------------------------------------
    # FEEDBACK LEARNING
    # -------------------------------------------------------------------------
    
    def feedback(self, 
                 text: str, 
                 sounds_like_me: bool,
                 strength: float = 1.0) -> Dict[str, Any]:
        """
        Learn from user feedback on generated text.
        
        Args:
            text: The generated text being evaluated
            sounds_like_me: True if user says it matches their voice
            strength: How strong the feedback is (0.5 = mild, 1.0 = strong)
        
        Returns:
            Updated signature stats
        """
        if not self.signature:
            raise ValueError("No signature to update")
        
        # Embed the feedback text
        embedding = self.embedder.embed([text])[0]
        current_similarity = self._cosine_similarity_single(
            embedding, np.array(self.signature.signature_vector)
        )
        
        # Update feedback counts
        if sounds_like_me:
            self.signature.positive_feedback += 1
            
            # Pull signature slightly toward this example
            old_vec = np.array(self.signature.signature_vector)
            adjustment = strength * 0.01 * (embedding - old_vec)
            new_vec = old_vec + adjustment
            self.signature.signature_vector = new_vec.tolist()
            
            # If similarity was below threshold but user approved, lower threshold
            if current_similarity < self.signature.similarity_threshold:
                self.signature.similarity_threshold = max(
                    0.3,  # Floor
                    self.signature.similarity_threshold - 0.02 * strength
                )
        else:
            self.signature.negative_feedback += 1
            
            # Push signature slightly away from this example
            old_vec = np.array(self.signature.signature_vector)
            adjustment = strength * 0.01 * (old_vec - embedding)
            new_vec = old_vec + adjustment
            self.signature.signature_vector = new_vec.tolist()
            
            # If similarity was above threshold but user rejected, raise threshold
            if current_similarity >= self.signature.similarity_threshold:
                self.signature.similarity_threshold = min(
                    0.95,  # Ceiling
                    self.signature.similarity_threshold + 0.02 * strength
                )
        
        # Update confidence based on feedback history
        total_feedback = self.signature.positive_feedback + self.signature.negative_feedback
        if total_feedback > 5:
            self.signature.confidence = min(
                0.98,
                self.signature.confidence + 0.01
            )
        
        self.signature.updated_at = datetime.now().isoformat()
        
        return {
            "similarity": current_similarity,
            "threshold": self.signature.similarity_threshold,
            "confidence": self.signature.confidence,
            "positive_feedback": self.signature.positive_feedback,
            "negative_feedback": self.signature.negative_feedback,
        }
    
    # -------------------------------------------------------------------------
    # EVALUATION
    # -------------------------------------------------------------------------
    
    def evaluate(self, text: str) -> Dict[str, Any]:
        """
        Evaluate how well text matches the learned voice.
        
        Returns:
            - similarity: 0-1 score
            - sounds_like_me: bool (above threshold)
            - confidence: how confident the evaluation is
            - contrast_scores: similarity to contrast examples (lower = better)
        """
        if not self.signature:
            raise ValueError("No signature loaded")
        
        # Embed text
        embedding = self.embedder.embed([text])[0]
        signature = np.array(self.signature.signature_vector)
        
        # Calculate similarity to voice signature
        similarity = self._cosine_similarity_single(embedding, signature)
        
        # Check against contrast vectors
        contrast_scores = {}
        for vec, label in zip(self.signature.contrast_vectors, self.signature.contrast_labels):
            contrast_scores[label] = self._cosine_similarity_single(
                embedding, np.array(vec)
            )
        
        # Calculate adjusted score (penalize similarity to contrasts)
        if contrast_scores:
            max_contrast = max(contrast_scores.values())
            adjusted_similarity = similarity - 0.3 * max_contrast
        else:
            adjusted_similarity = similarity
        
        return {
            "similarity": float(similarity),
            "adjusted_similarity": float(adjusted_similarity),
            "sounds_like_me": adjusted_similarity >= self.signature.similarity_threshold,
            "threshold": self.signature.similarity_threshold,
            "confidence": self.signature.confidence,
            "contrast_scores": contrast_scores,
        }
    
    def compare_texts(self, text_a: str, text_b: str) -> Dict[str, Any]:
        """Compare two texts to see which sounds more like the user"""
        if not self.signature:
            raise ValueError("No signature loaded")
        
        eval_a = self.evaluate(text_a)
        eval_b = self.evaluate(text_b)
        
        return {
            "text_a_similarity": eval_a["similarity"],
            "text_b_similarity": eval_b["similarity"],
            "closer_to_voice": "a" if eval_a["similarity"] > eval_b["similarity"] else "b",
            "difference": abs(eval_a["similarity"] - eval_b["similarity"]),
        }
    
    # -------------------------------------------------------------------------
    # PROMPT GENERATION
    # -------------------------------------------------------------------------
    
    def generate_voice_prompt(self, 
                              include_samples: bool = True,
                              n_samples: int = 3) -> str:
        """
        Generate a prompt that captures the voice signature.
        
        Unlike statistical constraints, this uses semantic description
        + exemplars to convey the voice.
        """
        if not self.signature:
            raise ValueError("No signature loaded")
        
        parts = []
        
        # Semantic description (let LLM interpret the signature)
        parts.append(f"""## VOICE SIGNATURE

You are writing in a specific person's voice. This voice has been learned from 
{self.signature.sample_count} samples ({self.signature.total_words:,} words total).

The voice signature has a confidence level of {self.signature.confidence:.0%}.
Similarity threshold: {self.signature.similarity_threshold:.2f}

When generating text, match the FEEL and RHYTHM of this writing, not just
surface features like word choice.""")
        
        # Contrastive guidance
        if self.signature.contrast_labels:
            parts.append(f"""
## WHAT THIS VOICE IS NOT

This voice has been contrasted against:
{', '.join(self.signature.contrast_labels)}

Actively avoid characteristics of these contrast categories.""")
        
        # Exemplars
        if include_samples and self._samples:
            parts.append("""
## VOICE EXEMPLARS

Study these examples carefully. Match their:
- Sentence rhythm and variation
- Level of formality and directness
- Way of making claims and hedging
- Integration of evidence and citations
- Authorial presence (I/we usage)
""")
            for i, sample in enumerate(self._samples[:n_samples], 1):
                excerpt = ' '.join(sample.split()[:400])
                parts.append(f"### Example {i}:\n{excerpt}\n")
        
        # Feedback-informed guidance
        if self.signature.positive_feedback > 0 or self.signature.negative_feedback > 0:
            parts.append(f"""
## LEARNED FROM FEEDBACK

This voice profile has been refined through {self.signature.positive_feedback + self.signature.negative_feedback} 
feedback instances. Trust the examples and constraints—they reflect what the 
author actually approves.""")
        
        return '\n\n'.join(parts)
    
    # -------------------------------------------------------------------------
    # UTILITIES
    # -------------------------------------------------------------------------
    
    def _cosine_similarity(self, embeddings: np.ndarray, target: np.ndarray) -> np.ndarray:
        """Cosine similarity between embeddings and target vector"""
        embeddings_norm = embeddings / np.linalg.norm(embeddings, axis=1, keepdims=True)
        target_norm = target / np.linalg.norm(target)
        return embeddings_norm @ target_norm
    
    def _cosine_similarity_single(self, a: np.ndarray, b: np.ndarray) -> float:
        """Cosine similarity between two vectors"""
        return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


# ============================================================================
# INTEGRATION WITH COMSCRIBE PIPELINE
# ============================================================================

class VoiceManager:
    """
    High-level interface for voice learning in CommScribe.
    
    Manages profiles, handles persistence, integrates with pipeline.
    """
    
    def __init__(self, profiles_dir: Path = None):
        self.profiles_dir = profiles_dir or Path.home() / ".commscribe" / "voices"
        self.profiles_dir.mkdir(parents=True, exist_ok=True)
        self.learner: Optional[AdaptiveVoiceLearner] = None
    
    def setup_voice(self, 
                    user_id: str,
                    samples: List[str],
                    contrast_samples: Dict[str, List[str]] = None) -> VoiceSignature:
        """
        Initial voice setup.
        
        Args:
            user_id: Identifier for this voice profile
            samples: List of user's writing samples
            contrast_samples: Optional dict of {label: [samples]} for contrastive learning
        """
        self.learner = AdaptiveVoiceLearner()
        
        # Learn from samples
        signature = self.learner.learn_from_samples(samples, user_id)
        
        # Add contrast if provided
        if contrast_samples:
            for label, texts in contrast_samples.items():
                self.learner.add_contrast(texts, label)
        
        # Save
        profile_path = self.profiles_dir / f"{user_id}.json"
        signature.save(profile_path)
        
        return signature
    
    def load_voice(self, user_id: str) -> Optional[VoiceSignature]:
        """Load existing voice profile"""
        profile_path = self.profiles_dir / f"{user_id}.json"
        if not profile_path.exists():
            return None
        
        self.learner = AdaptiveVoiceLearner()
        self.learner.signature = VoiceSignature.load(profile_path)
        return self.learner.signature
    
    def add_samples(self, user_id: str, samples: List[str]) -> VoiceSignature:
        """Add more samples to existing profile"""
        existing = self.load_voice(user_id)
        if not existing:
            return self.setup_voice(user_id, samples)
        
        self.learner = AdaptiveVoiceLearner()
        signature = self.learner.learn_from_samples(samples, user_id, existing)
        
        profile_path = self.profiles_dir / f"{user_id}.json"
        signature.save(profile_path)
        
        return signature
    
    def feedback(self, user_id: str, text: str, sounds_like_me: bool) -> Dict:
        """Process user feedback"""
        if not self.learner or not self.learner.signature:
            self.load_voice(user_id)
        
        if not self.learner:
            raise ValueError(f"No profile for {user_id}")
        
        result = self.learner.feedback(text, sounds_like_me)
        
        # Save updated profile
        profile_path = self.profiles_dir / f"{user_id}.json"
        self.learner.signature.save(profile_path)
        
        return result
    
    def evaluate(self, user_id: str, text: str) -> Dict:
        """Evaluate text against voice profile"""
        if not self.learner or not self.learner.signature:
            self.load_voice(user_id)
        
        if not self.learner:
            raise ValueError(f"No profile for {user_id}")
        
        return self.learner.evaluate(text)
    
    def get_prompt(self, user_id: str) -> str:
        """Get voice-constrained prompt for generation"""
        if not self.learner or not self.learner.signature:
            self.load_voice(user_id)
        
        if not self.learner:
            raise ValueError(f"No profile for {user_id}")
        
        return self.learner.generate_voice_prompt()


# ============================================================================
# CLI
# ============================================================================

if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("Adaptive Voice Learning - Test Mode")
    print("=" * 60)
    
    # Test samples
    test_samples = [
        """
        This study examines the evolution of networked gatekeeping in digital media 
        environments. Drawing on Meraz and Papacharissi's (2013) framework, we argue 
        that traditional gatekeeping models inadequately capture the distributed nature 
        of information control in social media contexts. Our analysis suggests that 
        algorithmic curation, user sharing behaviors, and platform affordances interact 
        to create emergent gatekeeping dynamics that differ substantially from legacy 
        media structures. However, we note several limitations in existing approaches.
        """,
        """
        The relationship between social media platforms and democratic discourse has 
        been extensively debated in recent scholarship. While some researchers emphasize 
        the democratizing potential of networked communication, others highlight the 
        risks of fragmentation and echo chambers. Our approach synthesizes these 
        perspectives by examining how platform architecture shapes the conditions of 
        possibility for public deliberation.
        """
    ]
    
    # AI contrast sample
    ai_sample = """
        In recent years, there has been a significant increase in the importance of 
        digital media in our daily lives. It is important to note that this transformation 
        has wide-ranging implications. Furthermore, the rise of social media platforms 
        has fundamentally changed how we communicate. Moreover, these changes have 
        impacted various aspects of society. Additionally, researchers have begun to 
        explore these phenomena. In conclusion, this is a crucial area of study.
    """
    
    manager = VoiceManager()
    
    try:
        # Setup voice with contrast
        print("\n📚 Learning voice from samples...")
        signature = manager.setup_voice(
            "test_user",
            test_samples,
            contrast_samples={"ai_generated": [ai_sample]}
        )
        
        print(f"\n✅ Voice signature created!")
        print(f"   Samples: {signature.sample_count}")
        print(f"   Words: {signature.total_words:,}")
        print(f"   Confidence: {signature.confidence:.0%}")
        print(f"   Threshold: {signature.similarity_threshold:.3f}")
        print(f"   Contrasts: {signature.contrast_labels}")
        
        # Evaluate the AI sample
        print("\n🔍 Evaluating AI-generated text...")
        eval_result = manager.evaluate("test_user", ai_sample)
        print(f"   Similarity: {eval_result['similarity']:.3f}")
        print(f"   Sounds like me: {eval_result['sounds_like_me']}")
        print(f"   Contrast scores: {eval_result['contrast_scores']}")
        
        # Evaluate original sample
        print("\n🔍 Evaluating original sample...")
        eval_result = manager.evaluate("test_user", test_samples[0])
        print(f"   Similarity: {eval_result['similarity']:.3f}")
        print(f"   Sounds like me: {eval_result['sounds_like_me']}")
        
        # Generate voice prompt
        print("\n📝 Voice prompt preview:")
        print("-" * 40)
        prompt = manager.get_prompt("test_user")
        print(prompt[:800] + "...")
        
        print("\n✅ Adaptive voice learning ready!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("(This is expected if no embedding provider is available)")
        print("\nTo use adaptive voice learning, install one of:")
        print("  pip install sentence-transformers")
        print("  ollama pull nomic-embed-text")
        print("  export OPENAI_API_KEY=...")
