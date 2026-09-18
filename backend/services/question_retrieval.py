"""
Zavran AI — Hybrid Question Retrieval & Multi-Level Deduplication Engine
Integrates:
1. Multi-path candidate pool retrieval (Exact Role, Semantic Role, Skill Match, Vector/Text Similarity)
2. Multi-level deduplication (Exact Hash + Near-Duplicate Semantic Similarity)
3. Deterministic ranking & diversity balancing
4. Answer quality validation
5. Provenance tracking (Hugging Face vs. Generated)
6. Hot Redis/Memory Caching
"""

import time
import re
import uuid
import logging
from typing import Dict, Any, List, Optional, Tuple, Set

from backend.models.question_source import QuestionSource, AnswerStatus, QualityStatus
from backend.models.interview_question import (
    NormalizedQuestion,
    InterviewPack,
    InterviewPackQuestion,
    generate_content_hash,
)
from backend.services.role_normalizer import RoleNormalizer
from backend.services.skill_extractor import SkillExtractor
from backend.services.question_validator import QuestionValidator
from backend.services.question_cache import question_cache
from backend.services.question_ranker import QuestionRanker, _compute_cosine_jaccard
from backend.question_bank import question_bank, compute_semantic_similarity

logger = logging.getLogger("ZavranAI.QuestionRetrieval")


def _normalize_text_for_hash(text: str) -> str:
    """Normalizes string for exact duplicate detection."""
    if not text:
        return ""
    t = text.lower().strip()
    t = re.sub(r"[^\w\s]", "", t)
    t = re.sub(r"\s+", " ", t)
    return t


class QuestionRetrievalEngine:
    """
    Hybrid Retrieval and Deduplication Engine preparing 100-question packs.
    """

    def __init__(self):
        self.bank = question_bank
        self.cache = question_cache

    def deduplicate_questions(
        self,
        questions: List[NormalizedQuestion],
        similarity_threshold: float = 0.80,
    ) -> List[NormalizedQuestion]:
        """
        Performs 2-stage deduplication:
        Stage 1: Exact normalized hash deduplication.
        Stage 2: Near-duplicate semantic overlap suppression (keeps higher quality score).
        """
        exact_seen: Set[str] = set()
        stage1_unique: List[NormalizedQuestion] = []

        # Stage 1: Exact hash
        for q in questions:
            norm_str = _normalize_text_for_hash(q.question)
            if not norm_str:
                continue
            h = q.content_hash or generate_content_hash(q.normalized_role, norm_str)
            if h not in exact_seen:
                exact_seen.add(h)
                stage1_unique.append(q)

        # Stage 2: Near duplicate semantic suppression
        deduped: List[NormalizedQuestion] = []
        for cand in stage1_unique:
            is_dup = False
            for existing in deduped:
                sim = compute_semantic_similarity(cand.question, existing.question)
                sim_tok = _compute_cosine_jaccard(cand.question, existing.question)
                effective_sim = max(sim, sim_tok)
                if effective_sim >= similarity_threshold or sim >= 0.55:
                    is_dup = True
                    # If incoming is higher quality, replace existing
                    if cand.quality_score > existing.quality_score:
                        deduped.remove(existing)
                        deduped.append(cand)
                    break
            if not is_dup:
                deduped.append(cand)

        return deduped

    def retrieve_candidate_pool(
        self,
        canonical_role: str,
        target_role: str,
        skills: List[str],
        difficulty: str = "Medium",
        seniority: str = "Mid-Level",
        limit_per_strategy: int = 150,
    ) -> List[NormalizedQuestion]:
        """
        Retrieves a wide candidate pool from persistent Question Bank across 4 paths:
        1. Exact Role Match
        2. Semantic/Fuzzy Role Match
        3. Skill Match
        4. Category & Quality General Match
        """
        pool: List[NormalizedQuestion] = []
        seen_ids: Set[str] = set()

        # Helper to convert raw DB row / dict to NormalizedQuestion
        def add_records(records: List[Dict[str, Any]]):
            for r in records:
                r_id = r.get("id") or str(uuid.uuid4())
                if r_id in seen_ids:
                    continue
                q_text = r.get("question", "")
                a_text = r.get("ideal_answer") or r.get("answer") or ""
                
                # Check validation
                valid, _ = QuestionValidator.validate_raw_record(r.get("role"), q_text, a_text)
                if not valid:
                    continue

                norm_role = r.get("normalized_role") or RoleNormalizer.normalize_role(r.get("role"))
                c_hash = r.get("content_hash") or generate_content_hash(norm_role, q_text)
                
                # Extract skills if not present
                q_skills = r.get("skills") or []
                if isinstance(q_skills, str):
                    try:
                        import json
                        q_skills = json.loads(q_skills)
                    except Exception:
                        q_skills = [s.strip() for s in q_skills.split(",") if s.strip()]

                if not q_skills:
                    q_skills = SkillExtractor.extract_skills_from_text(f"{q_text} {a_text}")

                nq = NormalizedQuestion(
                    id=r_id,
                    source=r.get("source") or QuestionSource.HUGGINGFACE.value,
                    dataset=r.get("dataset_name") or r.get("dataset") or "Ankshi/hr-interview-dataset",
                    role=r.get("role") or target_role,
                    normalized_role=norm_role,
                    question=q_text,
                    answer=a_text,
                    category=r.get("category") or "Technical",
                    difficulty=r.get("difficulty") or difficulty,
                    skills=q_skills,
                    content_hash=c_hash,
                    quality_score=float(r.get("quality_score") or 90.0),
                    created_at=float(r.get("created_at") or time.time()),
                    updated_at=float(r.get("updated_at") or time.time()),
                    dataset_version=int(r.get("dataset_version") or 1),
                )
                seen_ids.add(r_id)
                pool.append(nq)

        # Path 1: Exact Role
        r1 = self.bank.search_questions(role=target_role, limit=limit_per_strategy)
        add_records(r1)

        # Path 2: Canonical Role if different
        if canonical_role.lower() != target_role.lower():
            r2 = self.bank.search_questions(role=canonical_role, limit=limit_per_strategy)
            add_records(r2)

        # Path 3: Skill match
        if skills:
            r3 = self.bank.search_questions(skills=skills[:8], limit=limit_per_strategy)
            add_records(r3)

        # Path 4: Category/General fallback
        r4 = self.bank.search_questions(difficulty=difficulty, limit=limit_per_strategy)
        add_records(r4)

        return pool

    def prepare_100_question_pack(
        self,
        target_role: str,
        job_description: Optional[str] = None,
        resume_text: Optional[str] = None,
        seniority: str = "Mid-Level",
        required_skills: Optional[List[str]] = None,
        question_count: int = 100,
        interview_type: str = "Technical",
        use_cache: bool = True,
    ) -> InterviewPack:
        """
        Prepares a deterministic, role-relevant 100-question interview pack.
        Combines HF dataset records and existing generated question pool with strict provenance.
        """
        # Step 1: Role Normalization
        role_resolution = RoleNormalizer.resolve_candidate_role(target_role=target_role)
        canonical_role = role_resolution["canonical_role"]

        # Step 2: Skill Extraction
        skill_data = SkillExtractor.extract_from_profiles(
            role=target_role,
            jd_text=job_description,
            resume_text=resume_text,
            explicit_skills=required_skills or [],
        )
        all_skills = skill_data["all_skills"]
        jd_skills = skill_data["jd_skills"]
        resume_skills = skill_data["resume_skills"]

        # Step 3: Check Cache
        cache_key = self.cache.build_cache_key(
            normalized_role=canonical_role,
            seniority=seniority,
            skills=all_skills,
            version="v2",
        )
        if use_cache:
            cached_data = self.cache.get(cache_key)
            if cached_data:
                logger.info(f"Returning cached 100-question pack for {canonical_role}")
                return InterviewPack(**cached_data)

        # Step 4: Retrieve Candidate Pool
        candidate_pool = self.retrieve_candidate_pool(
            canonical_role=canonical_role,
            target_role=target_role,
            skills=all_skills,
            difficulty="Medium",
            seniority=seniority,
            limit_per_strategy=150,
        )

        # Step 5: Deduplicate
        deduped_pool = self.deduplicate_questions(candidate_pool, similarity_threshold=0.80)

        # Step 6: Rank & Balance
        query_context = f"{target_role} {job_description or ''} {' '.join(all_skills)}"
        ranked_pool = QuestionRanker.rank_and_balance_pool(
            candidates=deduped_pool,
            canonical_role=canonical_role,
            target_role=target_role,
            jd_skills=jd_skills,
            resume_skills=resume_skills,
            query_context=query_context,
            target_difficulty="Medium",
            target_count=question_count,
        )

        # Step 7: Answer Quality Validation
        validated_hf_questions: List[InterviewPackQuestion] = []
        hf_count = 0
        gen_count = 0

        for q in ranked_pool:
            is_valid, _ = QuestionValidator.validate_raw_record(q.role, q.question, q.answer)
            if is_valid:
                source_label = QuestionSource.HUGGINGFACE.value if q.source == QuestionSource.HUGGINGFACE.value else QuestionSource.GENERATED.value
                if source_label == QuestionSource.HUGGINGFACE.value:
                    hf_count += 1
                else:
                    gen_count += 1

                validated_hf_questions.append(
                    InterviewPackQuestion(
                        id=q.id,
                        question=q.question,
                        answer=q.answer,
                        category=q.category,
                        difficulty=q.difficulty,
                        source=source_label,
                        skills=q.skills,
                        role=q.role,
                        answer_status=AnswerStatus.VALIDATED.value,
                    )
                )

        # Step 8: If fewer than requested question_count, backfill from approved generated questions
        if len(validated_hf_questions) < question_count:
            # Check internal bank for generated questions or seed questions to safely complete the pack
            extra_questions = self.bank.search_questions(role=canonical_role, limit=question_count)
            for eq in extra_questions:
                if len(validated_hf_questions) >= question_count:
                    break
                eq_id = eq.get("id")
                if any(x.id == eq_id for x in validated_hf_questions):
                    continue
                q_text = eq.get("question", "")
                a_text = eq.get("ideal_answer") or eq.get("answer") or ""
                v, _ = QuestionValidator.validate_raw_record(canonical_role, q_text, a_text)
                if v:
                    gen_count += 1
                    validated_hf_questions.append(
                        InterviewPackQuestion(
                            id=eq_id or f"gen_{uuid.uuid4().hex[:12]}",
                            question=q_text,
                            answer=a_text,
                            category=eq.get("category") or "Technical",
                            difficulty=eq.get("difficulty") or "Medium",
                            source=QuestionSource.GENERATED.value,
                            skills=eq.get("skills") or [canonical_role],
                            role=canonical_role,
                            answer_status=AnswerStatus.GENERATED.value,
                        )
                    )

        pack_id = "pack_" + uuid.uuid4().hex[:12]
        pack = InterviewPack(
            interview_pack_id=pack_id,
            role=target_role,
            normalized_role=canonical_role,
            seniority=seniority,
            target_role=target_role,
            question_count=len(validated_hf_questions),
            source={
                "huggingface": hf_count,
                "generated": gen_count,
            },
            questions=validated_hf_questions[:question_count],
            cache_key=cache_key,
        )

        # Store in cache
        if use_cache:
            self.cache.set(cache_key, pack.dict(), ttl_seconds=86400)

        return pack


question_retrieval_engine = QuestionRetrievalEngine()
