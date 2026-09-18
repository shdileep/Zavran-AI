"""
Zavran AI — Normalized Interview Question Models
"""

import time
import hashlib
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from backend.models.question_source import QuestionSource, AnswerStatus, QualityStatus


def generate_content_hash(role: str, question: str) -> str:
    """Generates a deterministic SHA256 content hash for deduplication."""
    norm_text = f"{role.strip().lower()}:{question.strip().lower()}"
    return hashlib.sha256(norm_text.encode("utf-8")).hexdigest()


class NormalizedQuestion(BaseModel):
    id: str
    source: str = QuestionSource.HUGGINGFACE.value
    dataset: Optional[str] = "Ankshi/hr-interview-dataset"
    source_url: Optional[str] = "https://huggingface.co/datasets/Ankshi/hr-interview-dataset"
    role: str
    normalized_role: str
    question: str
    answer: str
    category: str = "Technical"
    difficulty: str = "Medium"
    skills: List[str] = Field(default_factory=list)
    content_hash: str
    answer_status: str = AnswerStatus.DATASET.value
    quality_status: str = QualityStatus.APPROVED.value
    quality_score: float = 90.0
    embedding: Optional[List[float]] = None
    created_at: float = Field(default_factory=time.time)
    updated_at: float = Field(default_factory=time.time)
    dataset_version: int = 1
    is_active: bool = True
    metadata: Dict[str, Any] = Field(default_factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        return self.dict()

    def to_candidate_safe_dict(self) -> Dict[str, Any]:
        """Candidate-safe representation with zero answer or rubric leakage."""
        return {
            "id": self.id,
            "question": self.question,
            "category": self.category,
            "difficulty": self.difficulty,
            "source": self.source,
            "role": self.role,
        }

    def to_evaluator_dict(self) -> Dict[str, Any]:
        """Backend evaluation-safe representation with answer and provenance."""
        return {
            "id": self.id,
            "question": self.question,
            "ideal_answer": self.answer,
            "answer": self.answer,
            "category": self.category,
            "difficulty": self.difficulty,
            "skills": self.skills,
            "source": self.source,
            "role": self.role,
            "normalized_role": self.normalized_role,
            "answer_status": self.answer_status,
            "quality_status": self.quality_status,
        }


class InterviewPackQuestion(BaseModel):
    id: str
    question: str
    answer: str
    category: str
    difficulty: str
    source: str
    skills: List[str] = Field(default_factory=list)
    role: Optional[str] = None
    answer_status: Optional[str] = None


class InterviewPack(BaseModel):
    interview_pack_id: str
    role: str
    normalized_role: str
    seniority: str
    target_role: str
    question_count: int
    source: Dict[str, int]
    questions: List[InterviewPackQuestion]
    created_at: float = Field(default_factory=time.time)
    cache_key: Optional[str] = None


class PrepareInterviewPackRequest(BaseModel):
    candidate_id: Optional[str] = None
    interview_id: Optional[str] = None
    candidate_name: Optional[str] = "Candidate"
    job_description: Optional[str] = ""
    resume_text: Optional[str] = ""
    resume_id: Optional[str] = None
    target_role: Optional[str] = "Full Stack AI Engineer"
    seniority: Optional[str] = "Mid-Level"
    required_skills: Optional[List[str]] = None
    question_count: int = 100
    interview_type: Optional[str] = "Technical"
    difficulty: Optional[str] = "Medium"
    clerk_user_id: Optional[str] = None
