"""
Zavran AI — Hugging Face Dataset Ingestion & Dynamic Mapping Engine
Dataset: Ankshi/hr-interview-dataset
Handles resilient schema inspection, column mapping, normalization, deduplication,
and batch ingestion with circuit breaker, timeout, and exponential backoff.
"""

import time
import json
import hashlib
import logging
import asyncio
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional, Tuple

from backend.models.question_source import QuestionSource, AnswerStatus, QualityStatus
from backend.models.interview_question import NormalizedQuestion, generate_content_hash
from backend.services.role_normalizer import RoleNormalizer
from backend.services.skill_extractor import SkillExtractor
from backend.services.question_validator import QuestionValidator

logger = logging.getLogger("ZavranAI.DatasetIngestion")

# Dynamic Column Mapping Layer
COLUMN_MAPPING = {
    "role": ["role", "job_role", "position", "title", "target_role"],
    "question": ["question", "interview_question", "prompt", "query", "text"],
    "answer": ["ideal_answer", "answer", "model_answer", "expected_answer", "response", "solution"],
    "category": ["category", "topic", "competency", "type", "source_type"],
    "difficulty": ["difficulty", "level", "seniority", "experience"],
    "skills": ["keywords", "skills", "tags", "technologies", "concepts"]
}

HF_ROWS_ENDPOINT = "https://datasets-server.huggingface.co/rows"
HF_SPLITS_ENDPOINT = "https://datasets-server.huggingface.co/splits"
HF_DATASET_NAME = "Ankshi/hr-interview-dataset"


class CircuitBreaker:
    """
    Lightweight Circuit Breaker protecting against cascading Hugging Face API failures.
    """
    def __init__(self, failure_threshold: int = 5, recovery_timeout: float = 60.0):
        self.failure_threshold = failure_threshold
        self.recovery_timeout = recovery_timeout
        self.failure_count = 0
        self.last_failure_time = 0.0
        self.state = "CLOSED"  # CLOSED, OPEN, HALF_OPEN

    def record_success(self):
        self.failure_count = 0
        self.state = "CLOSED"

    def record_failure(self):
        self.failure_count += 1
        self.last_failure_time = time.time()
        if self.failure_count >= self.failure_threshold:
            self.state = "OPEN"
            logger.warning("Circuit breaker OPENED for Hugging Face Dataset API.")

    def can_execute(self) -> bool:
        if self.state == "CLOSED":
            return True
        if self.state == "OPEN":
            if time.time() - self.last_failure_time > self.recovery_timeout:
                self.state = "HALF_OPEN"
                logger.info("Circuit breaker entered HALF_OPEN state.")
                return True
            return False
        return True  # HALF_OPEN


class DatasetIngestionService:
    """
    Service for ingesting, validating, and normalizing records from Ankshi/hr-interview-dataset.
    """

    def __init__(self, dataset_name: str = HF_DATASET_NAME):
        self.dataset_name = dataset_name
        self.circuit_breaker = CircuitBreaker()
        self.dataset_version = 1
        self.inferred_mapping: Dict[str, str] = {}

    def _extract_field(self, row_dict: Dict[str, Any], canonical_field: str) -> Any:
        """
        Dynamically extracts a field using the mapping layer or inferred schema.
        """
        candidates = COLUMN_MAPPING.get(canonical_field, [canonical_field])
        for cand in candidates:
            if cand in row_dict and row_dict[cand] is not None:
                return row_dict[cand]
        return None

    def map_and_normalize_row(self, raw_row: Dict[str, Any]) -> Optional[NormalizedQuestion]:
        """
        Transforms a raw Hugging Face row into a secure NormalizedQuestion instance.
        """
        if not raw_row or not isinstance(raw_row, dict):
            return None

        raw_q = self._extract_field(raw_row, "question")
        raw_a = self._extract_field(raw_row, "answer")
        raw_role = self._extract_field(raw_row, "role") or "Software Engineer"
        raw_cat = self._extract_field(raw_row, "category") or "Technical"
        raw_diff = self._extract_field(raw_row, "difficulty") or "Medium"
        raw_skills = self._extract_field(raw_row, "skills") or []

        # Validate quality & security
        is_valid, reason = QuestionValidator.validate_raw_record(raw_role, raw_q, raw_a)
        if not is_valid:
            logger.debug(f"Row rejected: {reason}")
            return None

        # Sanitize texts (treat as untrusted input)
        sanitized_q = QuestionValidator.sanitize_untrusted_text(str(raw_q))
        sanitized_a = QuestionValidator.sanitize_untrusted_text(str(raw_a))
        sanitized_role = QuestionValidator.sanitize_untrusted_text(str(raw_role))

        # Role normalization
        normalized_role = RoleNormalizer.normalize_role(sanitized_role)

        # Skill extraction & keywords combination
        skills_list = []
        if isinstance(raw_skills, list):
            skills_list.extend([str(k).strip() for k in raw_skills if str(k).strip()])
        elif isinstance(raw_skills, str):
            skills_list.extend([s.strip() for s in raw_skills.split(",") if s.strip()])

        extracted_skills = SkillExtractor.extract_skills_from_text(f"{sanitized_q} {sanitized_a} {sanitized_role}")
        combined_skills = list(dict.fromkeys(skills_list + extracted_skills))

        # Stable ID & Content Hash
        content_hash = generate_content_hash(normalized_role, sanitized_q)
        stable_id = f"hf_ankshi_{content_hash[:16]}"

        return NormalizedQuestion(
            id=stable_id,
            source=QuestionSource.HUGGINGFACE.value,
            dataset=self.dataset_name,
            source_url=f"https://huggingface.co/datasets/{self.dataset_name}",
            role=sanitized_role,
            normalized_role=normalized_role,
            question=sanitized_q,
            answer=sanitized_a,
            category=str(raw_cat).strip().capitalize(),
            difficulty=str(raw_diff).strip().capitalize(),
            skills=combined_skills,
            content_hash=content_hash,
            answer_status=AnswerStatus.DATASET.value,
            quality_status=QualityStatus.APPROVED.value,
            quality_score=90.0,
            dataset_version=self.dataset_version,
            is_active=True,
            metadata={
                "experience": raw_row.get("experience", "all"),
                "source_type": raw_row.get("source_type", "dataset")
            }
        )

    def fetch_rows_sync(
        self,
        offset: int = 0,
        length: int = 100,
        timeout: float = 5.0,
        max_retries: int = 3,
    ) -> List[Dict[str, Any]]:
        """
        Synchronously fetches a batch of rows from Hugging Face Dataset Server API
        with retries, exponential backoff, and circuit breaking.
        """
        if not self.circuit_breaker.can_execute():
            logger.warning("Hugging Face API circuit breaker is OPEN. Skipping API call.")
            return []

        url = f"{HF_ROWS_ENDPOINT}?dataset={urllib.parse.quote(self.dataset_name, safe='')}&config=default&split=train&offset={offset}&length={length}"
        backoff = 0.5

        for attempt in range(1, max_retries + 1):
            try:
                req = urllib.request.Request(
                    url,
                    headers={"User-Agent": "Zavran-AI-Ingestion-Worker/2.0"}
                )
                with urllib.request.urlopen(req, timeout=timeout) as response:
                    if response.status == 200:
                        data = json.loads(response.read().decode("utf-8"))
                        self.circuit_breaker.record_success()
                        rows = [r.get("row", {}) for r in data.get("rows", [])]
                        return rows
            except Exception as e:
                logger.warning(f"Fetch attempt {attempt}/{max_retries} failed for offset={offset}: {e}")
                time.sleep(backoff)
                backoff *= 2

        self.circuit_breaker.record_failure()
        return []

    async def fetch_and_normalize_batch(
        self,
        offset: int = 0,
        length: int = 100,
    ) -> List[NormalizedQuestion]:
        """
        Asynchronously fetches and normalizes a batch of dataset questions.
        """
        loop = asyncio.get_event_loop()
        raw_rows = await loop.run_in_executor(None, self.fetch_rows_sync, offset, length)
        normalized = []
        for r in raw_rows:
            norm = self.map_and_normalize_row(r)
            if norm:
                normalized.append(norm)
        return normalized
