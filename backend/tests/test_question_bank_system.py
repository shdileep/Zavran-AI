"""
Automated Test Suite for Zavran AI Question Bank & Assessment Studio System
Tests:
1. 200+ Role Catalog validation & uniqueness
2. Job Description understanding & skill extraction
3. Strict Question Quality Validator
4. Persistent Question Bank, Deduplication & Reuse
5. Dynamic Question Generation & Duration Planning
6. Adaptive Follow-up Engine & Dynamic Difficulty Progression
7. KimiProvider & Multi-LLM Failover Integration
8. Candidate Safety & Rubric Redaction Security
"""

import unittest
import asyncio
import json
import time

from backend.role_catalog import (
    get_all_roles,
    get_categories,
    get_roles_by_category,
    get_role_by_name,
    search_roles,
    get_total_role_count,
)
from backend.question_bank import (
    QuestionBank,
    compute_semantic_similarity,
)
from backend.question_generator import (
    QuestionGenerator,
    QuestionValidator,
)
from backend.providers.provider_factory import LLMProviderFactory
from backend.interview_engine import InterviewSession


class TestZavranQuestionBankSystem(unittest.TestCase):

    def setUp(self):
        self.bank = QuestionBank()
        self.generator = QuestionGenerator()

    # =========================================================================
    # 1. 200+ ROLE CATALOG TESTS
    # =========================================================================
    def test_01_role_catalog_count_and_uniqueness(self):
        roles = get_all_roles()
        total_count = get_total_role_count()
        self.assertGreaterEqual(total_count, 200, f"Role catalog must have >= 200 roles. Found: {total_count}")

        names = [r["name"].strip() for r in roles]
        self.assertEqual(len(names), len(set(names)), "Detected duplicate role names in catalog!")

        for r in roles:
            self.assertTrue(r["name"], "Role name is empty")
            self.assertTrue(r["category"], f"Role {r['name']} missing category")
            self.assertTrue(r["description"], f"Role {r['name']} missing description")
            self.assertGreaterEqual(len(r.get("common_skills", [])), 2, f"Role {r['name']} must have >= 2 common skills")

    def test_02_role_categories_and_search(self):
        categories = get_categories()
        self.assertGreaterEqual(len(categories), 20, "Must have at least 20 categories.")
        
        # Test category retrieval
        ai_roles = get_roles_by_category("AI & Machine Learning")
        self.assertGreater(len(ai_roles), 5)

        # Test search
        search_res = search_roles("Python", limit=10)
        self.assertGreater(len(search_res), 0)

        # Test exact role lookup
        role = get_role_by_name("Full Stack Engineer")
        self.assertIsNotNone(role)
        self.assertEqual(role["category"], "Software Engineering")

    # =========================================================================
    # 2. JOB DESCRIPTION UNDERSTANDING TESTS
    # =========================================================================
    def test_03_job_description_extraction(self):
        sample_jd = """
        Job Title: Senior AI Systems Engineer
        Requirements:
        - 4+ years building production AI applications using Python, FastAPI, and PostgreSQL.
        - Deep experience with Retrieval-Augmented Generation (RAG), Vector Databases (Pinecone/Qdrant), and LangChain.
        - Strong background in Docker, Redis caching, and Kubernetes microservices.
        Responsibilities:
        - Architect high-throughput LLM agentic workflows with low latency.
        """
        extracted = asyncio.run(self.generator.analyze_job_description(sample_jd))
        self.assertIn("Python", [s.title() for s in extracted["skills"]])
        self.assertTrue(any("RAG" in s.upper() or "FASTAPI" in s.upper() for s in extracted["skills"]))

    # =========================================================================
    # 3. QUESTION VALIDATION PIPELINE TESTS
    # =========================================================================
    def test_04_question_validator_rules(self):
        valid_q = {
            "question": "How do you mitigate context window overflow when streaming large token batches in FastAPI?",
            "ideal_answer": "By using token chunking estimators, prompt compression, and dynamic sliding context windows.",
            "difficulty": "medium",
            "expected_concepts": ["Sliding context window", "Token estimation", "Prompt compression"],
            "evaluation_criteria": ["Accuracy", "Experience"]
        }
        is_valid, issues = QuestionValidator.validate(valid_q)
        self.assertTrue(is_valid, f"Expected valid question, got issues: {issues}")

        # Invalid Question: placeholder and banned name
        invalid_q = {
            "question": "Ask candidate for {role} to describe their work at Zarun?",
            "ideal_answer": "",
            "difficulty": "invalid_diff",
            "expected_concepts": []
        }
        is_valid, issues = QuestionValidator.validate(invalid_q)
        self.assertFalse(is_valid)
        self.assertTrue(any("placeholder" in i for i in issues))
        self.assertTrue(any("Zarun" in i for i in issues))

    # =========================================================================
    # 4. INTERNAL QUESTION BANK & DEDUPLICATION TESTS
    # =========================================================================
    def test_05_question_bank_deduplication(self):
        q_original = {
            "id": "TEST-DEDUP-01",
            "role": "Cybersecurity Specialist",
            "category": "Offensive Security",
            "skill": "Penetration Testing",
            "difficulty": "hard",
            "seniority": "Senior",
            "question": "How do you systematically perform privilege escalation in Active Directory environments using Kerberoasting and AS-REP roasting?",
            "ideal_answer": "Requesting TGS service tickets for SPN accounts with weak passwords and cracking RC4/AES hashes offline, while querying accounts without pre-authentication required.",
            "expected_concepts": ["Kerberoasting", "AS-REP Roasting", "SPN scanning", "Ticket-Granting Service"],
            "evaluation_criteria": ["Offensive methodology", "Remediation protocols"],
            "verified": 1
        }
        saved1 = self.bank.save_question(q_original, reject_duplicates=False)
        self.assertIsNotNone(saved1)

        # Attempt to insert identical/duplicate question text
        q_duplicate = q_original.copy()
        q_duplicate["id"] = "TEST-DEDUP-02"
        q_duplicate["question"] = "How do you perform privilege escalation in Active Directory environments using Kerberoasting and AS-REP roasting?"
        
        saved2 = self.bank.save_question(q_duplicate, reject_duplicates=True)
        # Should reuse the existing question ID rather than creating a redundant row
        self.assertEqual(saved2["id"], "TEST-DEDUP-01")

    def test_06_similarity_scoring(self):
        t1 = "How do you optimize vector search index using HNSW in Pinecone?"
        t2 = "How do you optimize vector search index using HNSW in Pinecone databases?"
        t3 = "What is double-entry ledger bookkeeping in accounting?"

        sim_high = compute_semantic_similarity(t1, t2)
        sim_low = compute_semantic_similarity(t1, t3)

        self.assertGreater(sim_high, 0.75, "High similarity texts should score > 0.75")
        self.assertLess(sim_low, 0.20, "Unrelated texts should score < 0.20")

    # =========================================================================
    # 5. DYNAMIC QUESTION GENERATION & DURATION PLANNING
    # =========================================================================
    def test_07_duration_based_question_plan(self):
        # 15-minute interview -> 5 questions
        plan_15 = asyncio.run(self.generator.generate_interview_plan("Backend Developer", duration_minutes=15))
        self.assertEqual(len(plan_15), 5)

        # 30-minute interview -> 8 questions
        plan_30 = asyncio.run(self.generator.generate_interview_plan("Data Scientist", duration_minutes=30))
        self.assertEqual(len(plan_30), 8)

        # Assert questions have expected structured properties
        for p in plan_30:
            self.assertTrue(p.get("question"))
            self.assertTrue(p.get("difficulty"))
            self.assertTrue(p.get("category"))
            self.assertIn("hidden_rubric", p)

    # =========================================================================
    # 6. ADAPTIVE FOLLOW-UP ENGINE & DIFFICULTY PROGRESSION
    # =========================================================================
    def test_08_adaptive_followup_progression(self):
        current_q = {
            "question": "How do you reduce hallucinations in a RAG system?",
            "skill": "RAG Pipelines",
            "difficulty": "medium",
            "expected_concepts": ["Cross-encoder reranking", "Grounding benchmarks", "Context compression"]
        }

        # Case A: Weak answer -> should trigger basic/clarification follow-up
        weak_answer = "I don't know much about that."
        res_weak = asyncio.run(self.generator.evaluate_and_adapt_next(current_q, weak_answer, current_difficulty="medium"))
        self.assertTrue(res_weak["followup_needed"])
        self.assertEqual(res_weak["next_difficulty"], "easy")
        self.assertTrue(res_weak.get("adaptive_followup_question"))

        # Case B: Strong answer -> difficulty scaled up to hard
        strong_answer = "We use cross-encoder reranking with bge-reranker, semantic chunking, and strict Pydantic output schemas."
        res_strong = asyncio.run(self.generator.evaluate_and_adapt_next(current_q, strong_answer, current_difficulty="medium"))
        self.assertEqual(res_strong["next_difficulty"], "hard")

    # =========================================================================
    # 7. MULTI-LLM PROVIDER ARCHITECTURE (KIMI R3 SUPPORT)
    # =========================================================================
    def test_09_kimi_provider_and_fallback_failover(self):
        # Test Kimi provider instantiation
        kimi_p = LLMProviderFactory.get_provider("kimi")
        self.assertIsNotNone(kimi_p)
        self.assertEqual(kimi_p.__class__.__name__, "KimiProvider")

        # Test zero-failure fallback execution
        plan = asyncio.run(LLMProviderFactory.execute_with_fallback(
            "generate_interview_plan",
            {"name": "Test Candidate", "skills": ["Python"]},
            {"job_title": "AI Engineer", "required_skills": ["Python"]}
        ))
        self.assertIsInstance(plan, list)
        self.assertGreater(len(plan), 0)

    # =========================================================================
    # 8. SECURITY: CANDIDATE SAFETY & RUBRIC REDACTION
    # =========================================================================
    def test_10_candidate_safe_state_redaction(self):
        session = InterviewSession(
            interview_id="ZAV-SEC-99",
            candidate_name="Alex Mercer",
            target_role="AI Engineer"
        )
        safe_state = session.get_candidate_safe_state()

        # Verify candidate payload contains NO ideal answer or hidden internal rubrics
        safe_json = json.dumps(safe_state)
        self.assertNotIn("ideal_answer", safe_json)
        self.assertNotIn("unacceptable_misconceptions", safe_json)
        self.assertNotIn("red_flags", safe_json)
        self.assertNotIn("hidden_rubric", safe_json)


if __name__ == "__main__":
    unittest.main()
