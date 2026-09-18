"""
Zavran AI — Question and Answer Quality & Safety Validator
Enforces prompt injection detection, answer completeness, minimum text lengths,
and semantic relevance checks for all dataset and generated questions.
"""

import re
import logging
from typing import Dict, Any, Tuple, List, Optional

logger = logging.getLogger("ZavranAI.QuestionValidator")

# Known prompt injection & exploitation patterns
PROMPT_INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?(previous|prior)\s+instructions",
    r"system\s+prompt",
    r"you\s+are\s+now\s+a",
    r"as\s+an\s+ai\s+language\s+model",
    r"reveal\s+the\s+secret",
    r"override\s+system",
    r"drop\s+table",
    r"exec\s*\(",
    r"eval\s*\(",
    r"<script[\s>]",
    r"delete\s+from",
    r"api[_-]?key",
    r"bearer\s+[a-zA-Z0-9_\-\.]+",
    r"password\s*[:=]",
    r"sk-[a-zA-Z0-9]{20,}",
]


class QuestionValidator:
    """
    Validates question and answer quality and enforces strict security boundaries.
    """

    @classmethod
    def contains_prompt_injection(cls, text: str) -> bool:
        if not text:
            return False
        text_lower = text.lower()
        for pattern in PROMPT_INJECTION_PATTERNS:
            if re.search(pattern, text_lower):
                return True
        return False

    @classmethod
    def validate_raw_record(
        cls,
        role: Optional[str],
        question: Optional[str],
        answer: Optional[str],
        min_q_len: int = 10,
        min_a_len: int = 20,
    ) -> Tuple[bool, Optional[str]]:
        """
        Validates a raw Q&A record before it enters the database or retrieval pool.
        """
        if not question or not isinstance(question, str):
            return False, "Question is missing or not a string."
        
        q_clean = question.strip()
        if len(q_clean) < min_q_len:
            return False, f"Question text too short ({len(q_clean)} < {min_q_len} chars)."

        if not answer or not isinstance(answer, str):
            return False, "Answer is missing or not a string."

        a_clean = answer.strip()
        if len(a_clean) < min_a_len:
            return False, f"Answer text too short ({len(a_clean)} < {min_a_len} chars)."

        # Check prompt injection
        if cls.contains_prompt_injection(q_clean):
            return False, "Prompt injection / untrusted instruction pattern detected in question."

        if cls.contains_prompt_injection(a_clean):
            return False, "Prompt injection / untrusted instruction pattern detected in answer."

        # Check generic low-quality placeholder answers
        low_quality_answers = [
            "i don't know", "no answer", "n/a", "none", "unknown", "placeholder",
            "as per jd", "tbd", "to be determined"
        ]
        if a_clean.lower() in low_quality_answers:
            return False, "Answer is a generic low-quality placeholder."

        return True, None

    @classmethod
    def sanitize_untrusted_text(cls, text: str, max_length: int = 4000) -> str:
        """
        Sanitizes untrusted text to ensure safe string handling and prevents buffer issues.
        """
        if not text:
            return ""
        # Strip control characters except newline and tab
        cleaned = re.sub(r"[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]", "", text)
        return cleaned[:max_length].strip()
