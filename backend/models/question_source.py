"""
Zavran AI — Question Source & Provenance Models
"""

from enum import Enum


class QuestionSource(str, Enum):
    HUGGINGFACE = "huggingface"
    GENERATED = "generated"
    INTERNAL_BANK = "internal_bank"
    LLM_GENERATED = "llm_generated"
    SEEDED = "seeded"


class AnswerStatus(str, Enum):
    DATASET = "dataset"
    GENERATED = "generated"
    MISSING = "missing"
    VALIDATED = "validated"
    REJECTED = "rejected"


class QualityStatus(str, Enum):
    VERIFIED = "verified"
    APPROVED = "approved"
    PENDING = "pending"
    REJECTED = "rejected"
