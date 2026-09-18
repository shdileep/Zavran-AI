"""
Zavran AI — Deterministic Question Ranking & Diversity Balancing Engine
Scores questions based on 7 weighted multi-factor dimensions:
1. Role exact match (30%)
2. JD skill match (25%)
3. Resume skill match (15%)
4. Semantic similarity (15%)
5. Difficulty fit (5%)
6. Category balance (5%)
7. Question quality (5%)
"""

import math
import re
from typing import Dict, Any, List, Optional
from backend.models.interview_question import NormalizedQuestion
from backend.services.role_normalizer import RoleNormalizer


def _compute_cosine_jaccard(text1: str, text2: str) -> float:
    """Computes fast token overlap similarity between two text strings."""
    if not text1 or not text2:
        return 0.0
    t1 = set(re.findall(r"\w+", text1.lower()))
    t2 = set(re.findall(r"\w+", text2.lower()))
    if not t1 or not t2:
        return 0.0
    inter = len(t1.intersection(t2))
    union = len(t1.union(t2))
    return inter / union if union > 0 else 0.0


class QuestionRanker:
    """
    Ranks candidate questions deterministically and balances the final selection across categories.
    """

    @classmethod
    def calculate_score(
        cls,
        question: NormalizedQuestion,
        canonical_role: str,
        target_role: str,
        jd_skills: List[str],
        resume_skills: List[str],
        query_context: str,
        target_difficulty: str = "Medium",
        category_counts: Optional[Dict[str, int]] = None,
        target_category_dist: Optional[Dict[str, int]] = None,
    ) -> float:
        """
        Calculates deterministic composite relevance score in [0.0, 1.0].
        """
        q_role_norm = question.normalized_role.lower()
        can_role_norm = canonical_role.lower()
        target_role_norm = target_role.lower()

        # 1. Role Exact Match (30%)
        if q_role_norm == can_role_norm or q_role_norm == target_role_norm:
            role_score = 1.0
        elif can_role_norm in q_role_norm or q_role_norm in can_role_norm:
            role_score = 0.8
        elif any(w in q_role_norm for w in can_role_norm.split()):
            role_score = 0.4
        else:
            role_score = 0.1

        # 2. JD Skill Match (25%)
        q_skills_lower = [s.lower() for s in question.skills]
        q_text_lower = f"{question.question} {question.answer}".lower()
        
        jd_matches = 0
        if jd_skills:
            for sk in jd_skills:
                sk_l = sk.lower()
                if sk_l in q_skills_lower or sk_l in q_text_lower:
                    jd_matches += 1
            jd_score = min(1.0, jd_matches / max(1, min(len(jd_skills), 6)))
        else:
            jd_score = 0.7  # Default neutral score if no JD skills

        # 3. Resume Skill Match (15%)
        resume_matches = 0
        if resume_skills:
            for sk in resume_skills:
                sk_l = sk.lower()
                if sk_l in q_skills_lower or sk_l in q_text_lower:
                    resume_matches += 1
            resume_score = min(1.0, resume_matches / max(1, min(len(resume_skills), 6)))
        else:
            resume_score = 0.7

        # 4. Semantic Similarity (15%)
        sem_score = _compute_cosine_jaccard(question.question, query_context)

        # 5. Difficulty Fit (5%)
        q_diff = question.difficulty.lower()
        t_diff = target_difficulty.lower()
        if q_diff == t_diff or t_diff == "all":
            diff_score = 1.0
        elif (t_diff == "senior" and q_diff in ["hard", "expert", "medium"]) or (t_diff == "entry" and q_diff in ["easy", "medium"]):
            diff_score = 0.8
        else:
            diff_score = 0.5

        # 6. Category Balance (5%)
        cat = question.category
        cat_score = 1.0
        if category_counts and target_category_dist:
            target_cap = target_category_dist.get(cat, 15)
            current = category_counts.get(cat, 0)
            if current >= target_cap:
                cat_score = 0.2  # Penalize over-represented category
            else:
                cat_score = 1.0 - (current / max(1, target_cap)) * 0.5

        # 7. Question Quality (5%)
        quality_score = min(1.0, max(0.0, question.quality_score / 100.0))

        # Composite Weighted Total
        total_score = (
            0.30 * role_score +
            0.25 * jd_score +
            0.15 * resume_score +
            0.15 * sem_score +
            0.05 * diff_score +
            0.05 * cat_score +
            0.05 * quality_score
        )

        return round(total_score, 4)

    @classmethod
    def rank_and_balance_pool(
        cls,
        candidates: List[NormalizedQuestion],
        canonical_role: str,
        target_role: str,
        jd_skills: List[str],
        resume_skills: List[str],
        query_context: str,
        target_difficulty: str = "Medium",
        target_count: int = 100,
    ) -> List[NormalizedQuestion]:
        """
        Ranks the candidates using multi-factor scoring and ensures balanced category distribution.
        """
        if not candidates:
            return []

        # Get target category distribution for role
        role_info = RoleNormalizer.resolve_candidate_role(target_role=target_role)
        raw_dist = role_info.get("category_distribution", {})
        
        # Scale distribution to target_count
        target_category_dist: Dict[str, int] = {}
        total_dist_weight = sum(raw_dist.values()) or 100
        for cat, weight in raw_dist.items():
            target_category_dist[cat] = max(1, int(round((weight / total_dist_weight) * target_count)))

        scored_candidates: List[tuple] = []
        for q in candidates:
            score = cls.calculate_score(
                question=q,
                canonical_role=canonical_role,
                target_role=target_role,
                jd_skills=jd_skills,
                resume_skills=resume_skills,
                query_context=query_context,
                target_difficulty=target_difficulty,
                target_category_dist=target_category_dist,
            )
            scored_candidates.append((score, q))

        # Sort descending by score
        scored_candidates.sort(key=lambda x: x[0], reverse=True)

        # Select with category balance enforcement
        selected: List[NormalizedQuestion] = []
        category_counts: Dict[str, int] = {}
        remaining: List[NormalizedQuestion] = []

        for score, q in scored_candidates:
            cat = q.category
            current = category_counts.get(cat, 0)
            cap = target_category_dist.get(cat, 20)
            if current < cap and len(selected) < target_count:
                selected.append(q)
                category_counts[cat] = current + 1
            else:
                remaining.append(q)

        # If we haven't reached target_count yet, backfill from remaining high-scoring candidates
        if len(selected) < target_count and remaining:
            backfill_needed = target_count - len(selected)
            selected.extend(remaining[:backfill_needed])

        return selected[:target_count]
