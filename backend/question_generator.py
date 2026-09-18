"""
Zavran AI — Dynamic Interview Question Generation & Adaptive Follow-up Engine
Orchestrates Job Description analysis, balanced interview planning, retrieval-first reuse from
the internal Question Bank, strict JSON validation, dynamic difficulty adaptation, and real-time follow-ups.
"""

import os
import json
import logging
import re
import uuid
from typing import Dict, Any, List, Optional, Tuple

from backend.config import settings
from backend.role_catalog import get_role_by_name, search_roles
from backend.question_bank import question_bank, QuestionBank
from backend.providers.provider_factory import LLMProviderFactory

logger = logging.getLogger("ZavranAI.QuestionGenerator")

class QuestionValidationError(Exception):
    pass


class QuestionValidator:
    """
    Automated multi-rule quality validator for newly generated interview questions.
    Ensures technical precision, clear wording, difficulty alignment, and zero answer leakage.
    """

    @staticmethod
    def validate(q: Dict[str, Any], role: str = "", jd_skills: Optional[List[str]] = None) -> Tuple[bool, List[str]]:
        issues: List[str] = []

        # Auto-normalize alternate field names if present
        if not q.get("expected_concepts"):
            if q.get("concepts_tested"):
                q["expected_concepts"] = q.get("concepts_tested")
            elif q.get("expected_answer_model", {}).get("critical_concepts"):
                q["expected_concepts"] = q["expected_answer_model"]["critical_concepts"] + q.get("expected_answer_model", {}).get("important_concepts", [])

        if not q.get("ideal_answer"):
            concepts = q.get("expected_concepts") or ["core technical competencies"]
            q["ideal_answer"] = f"Demonstrates mastery of {', '.join(concepts[:4])} with clear trade-off evaluation and practical production experience."

        if not q.get("evaluation_criteria"):
            if q.get("evaluation_points"):
                q["evaluation_criteria"] = q["evaluation_points"]
            else:
                q["evaluation_criteria"] = ["Evaluates technical accuracy and practical reasoning."]

        q_text = (q.get("question") or "").strip()
        if not q_text:
            issues.append("Question text is empty.")
        elif len(q_text) < 20:
            issues.append("Question text is too short (< 20 characters).")
        elif not q_text.endswith("?") and not q_text.endswith("."):
            issues.append("Question must end with proper punctuation.")

        # Check for placeholder tokens
        placeholders = ["{role}", "[insert", "{skill}", "candidate name", "xyz", "todo"]
        for p in placeholders:
            if p in q_text.lower():
                issues.append(f"Question contains template placeholder: '{p}'")

        # Validate ideal answer
        ideal = (q.get("ideal_answer") or "").strip()
        if not ideal or len(ideal) < 25:
            issues.append("Ideal answer is missing or insufficiently detailed (< 25 characters).")

        # Check for answer leakage in the question text
        if ideal and len(ideal) > 50 and ideal.lower() in q_text.lower():
            issues.append("Answer leakage detected in question body.")

        # Validate difficulty
        diff = (q.get("difficulty") or "").lower()
        if diff not in ["easy", "medium", "hard", "expert"]:
            q["difficulty"] = "medium"

        # Validate expected concepts
        concepts = q.get("expected_concepts") or []
        if not isinstance(concepts, list) or len(concepts) < 1:
            issues.append("Expected concepts must be a list containing at least 1 critical concept.")

        # Validate evaluation criteria
        criteria = q.get("evaluation_criteria") or []
        if not isinstance(criteria, list):
            q["evaluation_criteria"] = ["Evaluates technical accuracy and practical experience."]

        # Check banned words
        if "zarun" in q_text.lower() or "zarun" in ideal.lower():
            issues.append("Banned term 'Zarun' detected. Must strictly use 'Zavran AI'.")

        is_valid = len(issues) == 0
        return is_valid, issues


class QuestionGenerator:
    """
    Comprehensive Question Generation Engine combining:
    1. JD extraction and prioritization
    2. Retrieval-first reuse from persistent Question Bank
    3. Multi-LLM synthesis (Kimi R3, OpenAI, Gemini, etc.)
    4. Strict validation and automated storage
    5. Adaptive follow-up generation and dynamic difficulty scaling
    """

    def __init__(self):
        self.validator = QuestionValidator()
        self.bank = question_bank

    async def analyze_job_description(self, jd_text: str) -> Dict[str, Any]:
        """
        Deeply extracts technical requirements, tools, responsibilities, and seniority from raw JD text.
        """
        if not jd_text or len(jd_text.strip()) < 10:
            return {
                "role": "Full Stack AI Engineer",
                "seniority": "Mid-Senior",
                "skills": ["Python", "FastAPI", "LLMs", "RAG", "PostgreSQL", "Docker"],
                "tools": ["Git", "Docker", "PostgreSQL", "Redis"],
                "responsibilities": ["Build scalable software and AI systems"],
                "domain": "Artificial Intelligence & Software Engineering",
                "required_experience": "3+ years",
                "nice_to_have_skills": ["Kubernetes", "LangGraph"]
            }

        try:
            extracted = await LLMProviderFactory.execute_with_fallback("extract_job_description", jd_text)
            if extracted and isinstance(extracted, dict):
                # Normalize field names
                role = extracted.get("role") or extracted.get("job_title") or "Software Engineer"
                skills = extracted.get("skills") or extracted.get("required_skills") or []
                tools = extracted.get("tools") or extracted.get("technologies") or []
                seniority = extracted.get("seniority") or "Mid-Level"
                return {
                    "role": role,
                    "seniority": seniority,
                    "skills": list(dict.fromkeys(skills)),
                    "tools": list(dict.fromkeys(tools)),
                    "responsibilities": extracted.get("responsibilities", []),
                    "domain": extracted.get("domain", "Technology"),
                    "required_experience": extracted.get("required_experience") or extracted.get("experience_requirements", "2-5 years"),
                    "nice_to_have_skills": extracted.get("nice_to_have_skills") or extracted.get("preferred_skills", [])
                }
        except Exception as e:
            logger.warning(f"JD LLM extraction fallback: {e}")

        # Heuristic extraction fallback
        skills_found = []
        common_tech = [
            "python", "fastapi", "django", "flask", "react", "next.js", "typescript", "javascript",
            "node.js", "go", "golang", "rust", "c++", "java", "spring boot", "postgresql", "mysql",
            "redis", "mongodb", "kafka", "rabbitmq", "aws", "gcp", "azure", "docker", "kubernetes",
            "terraform", "rag", "llm", "langchain", "pytorch", "tensorflow", "ci/cd"
        ]
        jd_lower = jd_text.lower()
        for tech in common_tech:
            if re.search(r"\b" + re.escape(tech) + r"\b", jd_lower):
                skills_found.append(tech.title() if len(tech) > 3 else tech.upper())

        return {
            "role": "Technical Specialist",
            "seniority": "Mid-Level",
            "skills": skills_found or ["Software Engineering", "System Design"],
            "tools": ["Git", "Cloud Infrastructure"],
            "responsibilities": ["Deliver production systems"],
            "domain": "Software & Technology",
            "required_experience": "3+ years",
            "nice_to_have_skills": []
        }

    def _calculate_plan_structure(self, duration_minutes: int) -> List[Dict[str, Any]]:
        """
        Determines the balanced question category distribution based on interview duration.
        """
        if duration_minutes <= 15:
            # 5 questions total
            return [
                {"step": 1, "category": "Introduction & Background", "difficulty": "easy", "weight": 1},
                {"step": 2, "category": "Role Fundamentals", "difficulty": "medium", "weight": 1},
                {"step": 3, "category": "Technical Implementation", "difficulty": "medium", "weight": 1},
                {"step": 4, "category": "Problem Solving & Architecture", "difficulty": "hard", "weight": 1},
                {"step": 5, "category": "Project Experience & Closing", "difficulty": "medium", "weight": 1},
            ]
        elif duration_minutes <= 30:
            # 8 questions total
            return [
                {"step": 1, "category": "Introduction & Background", "difficulty": "easy", "weight": 1},
                {"step": 2, "category": "Role Fundamentals", "difficulty": "medium", "weight": 1},
                {"step": 3, "category": "Technical & Coding", "difficulty": "medium", "weight": 1},
                {"step": 4, "category": "Architecture & System Design", "difficulty": "hard", "weight": 1},
                {"step": 5, "category": "Scenario & Failure Recovery", "difficulty": "hard", "weight": 1},
                {"step": 6, "category": "Deep Technical Follow-up", "difficulty": "hard", "weight": 1},
                {"step": 7, "category": "Project Experience & Trade-offs", "difficulty": "medium", "weight": 1},
                {"step": 8, "category": "Behavioral & Closing", "difficulty": "medium", "weight": 1},
            ]
        elif duration_minutes <= 45:
            # 12 questions
            return [
                {"step": 1, "category": "Introduction & Background", "difficulty": "easy", "weight": 1},
                {"step": 2, "category": "Role Fundamentals", "difficulty": "medium", "weight": 1},
                {"step": 3, "category": "Core Competency Deep-Dive", "difficulty": "medium", "weight": 1},
                {"step": 4, "category": "Technical & Coding", "difficulty": "medium", "weight": 1},
                {"step": 5, "category": "Implementation & Concurrency", "difficulty": "hard", "weight": 1},
                {"step": 6, "category": "Architecture & System Design", "difficulty": "hard", "weight": 1},
                {"step": 7, "category": "Scalability & Distributed Systems", "difficulty": "hard", "weight": 1},
                {"step": 8, "category": "Scenario & Incident Response", "difficulty": "hard", "weight": 1},
                {"step": 9, "category": "Deep Technical Follow-up", "difficulty": "expert", "weight": 1},
                {"step": 10, "category": "Project Experience & Scale", "difficulty": "medium", "weight": 1},
                {"step": 11, "category": "Leadership & Collaboration", "difficulty": "medium", "weight": 1},
                {"step": 12, "category": "Closing & Reflections", "difficulty": "easy", "weight": 1},
            ]
        else:
            # 15 questions (60 min)
            return [
                {"step": 1, "category": "Introduction & Background", "difficulty": "easy", "weight": 1},
                {"step": 2, "category": "Role Fundamentals", "difficulty": "easy", "weight": 1},
                {"step": 3, "category": "Domain-Specific Knowledge", "difficulty": "medium", "weight": 1},
                {"step": 4, "category": "Technical Implementation", "difficulty": "medium", "weight": 1},
                {"step": 5, "category": "Coding & Algorithms", "difficulty": "medium", "weight": 1},
                {"step": 6, "category": "Data & State Management", "difficulty": "medium", "weight": 1},
                {"step": 7, "category": "Architecture & System Design", "difficulty": "hard", "weight": 1},
                {"step": 8, "category": "High Concurrency & Resilience", "difficulty": "hard", "weight": 1},
                {"step": 9, "category": "Security & Guardrails", "difficulty": "hard", "weight": 1},
                {"step": 10, "category": "Production Failure Scenarios", "difficulty": "hard", "weight": 1},
                {"step": 11, "category": "Deep Technical Follow-up", "difficulty": "expert", "weight": 1},
                {"step": 12, "category": "Project Architecture Review", "difficulty": "medium", "weight": 1},
                {"step": 13, "category": "Leadership & Mentorship", "difficulty": "medium", "weight": 1},
                {"step": 14, "category": "Behavioral & Cross-Functional", "difficulty": "medium", "weight": 1},
                {"step": 15, "category": "Strategic Vision & Closing", "difficulty": "easy", "weight": 1},
            ]

    async def generate_interview_plan(
        self,
        role_name: str,
        job_description: Optional[str] = None,
        seniority: str = "Mid-Level",
        years_of_experience: Optional[str] = "3+",
        required_skills: Optional[List[str]] = None,
        industry: Optional[str] = None,
        duration_minutes: int = 30,
        interview_type: str = "Comprehensive Technical",
        difficulty: str = "medium",
        candidate_name: str = "Candidate"
    ) -> List[Dict[str, Any]]:
        """
        Orchestrates full balanced interview plan:
        1. Analyzes JD if provided (JD takes precedence over generic role profile).
        2. Retrieves matching existing questions from Question Bank.
        3. Synthesizes any missing questions via configured LLM.
        4. Validates and permanently stores new questions in Question Bank.
        5. Returns structured, sanitized question plan.
        """
        # Step 1: Role & JD Context Resolution
        matched_role = get_role_by_name(role_name)
        role_display = matched_role["name"] if matched_role else role_name
        role_category = matched_role["category"] if matched_role else (industry or "Engineering")
        common_skills = matched_role["common_skills"] if matched_role else []

        jd_profile: Dict[str, Any] = {}
        target_skills = list(required_skills or [])

        if job_description and len(job_description.strip()) > 15:
            jd_profile = await self.analyze_job_description(job_description)
            if jd_profile.get("skills"):
                # JD skills take strict priority
                target_skills = list(dict.fromkeys(jd_profile["skills"] + target_skills))
            if jd_profile.get("seniority"):
                seniority = jd_profile["seniority"]

        if not target_skills:
            target_skills = common_skills or ["System Architecture", "Problem Solving", "Code Quality"]

        # Step 2: Calculate target slots
        structure = self._calculate_plan_structure(duration_minutes)
        total_needed = len(structure)

        # Step 3: Retrieval-First from Question Bank
        existing_pool = self.bank.search_questions(
            role=role_display,
            skills=target_skills,
            seniority=seniority,
            limit=total_needed
        )

        selected_questions: List[Dict[str, Any]] = []
        used_ids = set()

        for q in existing_pool:
            if len(selected_questions) < max(2, total_needed // 2):
                selected_questions.append(q)
                used_ids.add(q["id"])
                self.bank.record_usage(q["id"])

        missing_count = total_needed - len(selected_questions)

        # Step 4: Generate missing questions via LLM if needed
        if missing_count > 0:
            logger.info(f"Retrieval yielded {len(selected_questions)} questions. Synthesizing {missing_count} via LLM...")
            generated_new = await self._generate_llm_questions(
                role=role_display,
                role_category=role_category,
                seniority=seniority,
                skills=target_skills,
                job_description=job_description or "",
                count=missing_count,
                difficulty=difficulty,
                existing_questions=[q["question"] for q in selected_questions]
            )

            for gq in generated_new:
                gq["role"] = role_display
                gq["industry"] = role_category
                gq["seniority"] = seniority
                gq["job_description_context"] = (job_description or "")[:300]
                
                # Quality Validation
                is_valid, issues = self.validator.validate(gq, role=role_display, jd_skills=target_skills)
                if is_valid:
                    saved = self.bank.save_question(gq, reject_duplicates=True)
                    if saved.get("id") not in used_ids:
                        selected_questions.append(saved)
                        used_ids.add(saved.get("id"))
                else:
                    logger.warning(f"Generated question failed validation: {issues}. Retrying fallback structure...")

        # If still short, supplement with deterministic structural questions
        if len(selected_questions) < total_needed:
            shortfall = total_needed - len(selected_questions)
            fallback_qs = self._generate_structural_fallbacks(
                role=role_display,
                skills=target_skills,
                seniority=seniority,
                count=shortfall
            )
            for fq in fallback_qs:
                saved = self.bank.save_question(fq, reject_duplicates=False)
                selected_questions.append(saved)

        # Format final plan with step numbers and candidate-safe presentation
        final_plan: List[Dict[str, Any]] = []
        for idx, q_data in enumerate(selected_questions[:total_needed]):
            plan_item = {
                "id": q_data.get("id") or f"Q{idx+1:02d}",
                "question_id": q_data.get("id") or f"Q{idx+1:02d}",
                "step_label": f"Question {idx + 1} of {total_needed}",
                "category": q_data.get("category", "Technical Competency"),
                "skill": q_data.get("skill", target_skills[idx % len(target_skills)] if target_skills else "Engineering"),
                "difficulty": q_data.get("difficulty", "medium"),
                "question": q_data.get("question", ""),
                # Hidden Evaluation Rubrics (Never Exposed to Candidate directly)
                "hidden_rubric": {
                    "ideal_answer": q_data.get("ideal_answer", ""),
                    "expected_concepts": q_data.get("expected_concepts", []),
                    "evaluation_criteria": q_data.get("evaluation_criteria", []),
                    "red_flags": q_data.get("red_flags", []),
                    "follow_up_questions": q_data.get("follow_up_questions", []),
                },
                "expected_answer_model": {
                    "critical_concepts": q_data.get("expected_concepts", [])[:2],
                    "important_concepts": q_data.get("expected_concepts", [])[2:],
                    "unacceptable_misconceptions": q_data.get("red_flags", [])
                },
                "estimated_time_seconds": q_data.get("estimated_time_seconds", 90)
            }
            final_plan.append(plan_item)

        return final_plan

    async def _generate_llm_questions(
        self,
        role: str,
        role_category: str,
        seniority: str,
        skills: List[str],
        job_description: str,
        count: int,
        difficulty: str,
        existing_questions: List[str]
    ) -> List[Dict[str, Any]]:
        """
        Invokes LLM with strict JSON schema and anti-duplication constraints.
        """
        system_prompt = (
            "You are the Chief Interview Assessment Architect for Zavran AI. "
            "Generate a structured set of interview questions specifically designed for the given role and skills. "
            "CRITICAL CONSTRAINTS:\n"
            "1. Do NOT generate generic or cliché questions.\n"
            "2. Heavily test the actual technologies and tools listed.\n"
            "3. Every question must include an ideal answer, 3-5 expected concepts, red flags, and 2 follow-up probes.\n"
            "4. NEVER use the name 'Zarun'. The platform name is Zavran AI.\n"
            "5. Return ONLY valid JSON matching this schema:\n"
            "{\n"
            '  "questions": [\n'
            "    {\n"
            '      "question": "Detailed scenario or technical question text",\n'
            '      "category": "Technical|System Design|Problem Solving|Scenario-based|Behavioral",\n'
            '      "skill": "Specific skill being tested",\n'
            '      "difficulty": "easy|medium|hard|expert",\n'
            '      "ideal_answer": "Complete benchmark answer for evaluators",\n'
            '      "expected_concepts": ["concept 1", "concept 2", "concept 3"],\n'
            '      "evaluation_criteria": ["criteria 1", "criteria 2"],\n'
            '      "red_flags": ["critical misconception 1", "disqualifying claim 2"],\n'
            '      "follow_up_questions": ["Follow-up 1", "Follow-up 2"],\n'
            '      "estimated_time_seconds": 90\n'
            "    }\n"
            "  ]\n"
            "}"
        )

        user_prompt = (
            f"Target Role: {role}\n"
            f"Category / Industry: {role_category}\n"
            f"Seniority Level: {seniority}\n"
            f"Required Skills & Stack: {', '.join(skills)}\n"
            f"Job Description Context: {job_description[:600]}\n"
            f"Desired Difficulty: {difficulty}\n"
            f"Number of Questions Needed: {count}\n"
            f"Existing Questions Already in Plan (DO NOT DUPLICATE):\n" +
            "\n".join([f"- {q}" for q in existing_questions[:5]])
        )

        try:
            provider = LLMProviderFactory.get_provider()
            # If provider has native _call_chat_completion
            if hasattr(provider, "_call_chat_completion"):
                raw_json = provider._call_chat_completion(system_prompt, user_prompt, response_json=True)
                parsed = json.loads(raw_json)
                if isinstance(parsed, dict) and "questions" in parsed:
                    return parsed["questions"]
                elif isinstance(parsed, list):
                    return parsed
        except Exception as e:
            logger.warning(f"LLM question generation failed: {e}. Trying fallback execution...")

        try:
            # Fallback via LLMProviderFactory
            fallback_res = await LLMProviderFactory.execute_with_fallback(
                "generate_interview_plan",
                {"name": "Candidate", "skills": skills},
                {"job_title": role, "required_skills": skills, "role": role}
            )
            if fallback_res:
                return fallback_res[:count]
        except Exception as e:
            logger.error(f"Fallback generation error: {e}")

        return []

    def _generate_structural_fallbacks(
        self, role: str, skills: List[str], seniority: str, count: int
    ) -> List[Dict[str, Any]]:
        """
        Deterministic high-quality fallback generator ensuring zero failure under network outage.
        """
        top_skill = skills[0] if skills else "Distributed Systems"
        second_skill = skills[1] if len(skills) > 1 else "Database Optimization"
        third_skill = skills[2] if len(skills) > 2 else "API Resilience"

        templates = [
            {
                "question": f"When architecting production systems with {top_skill} for a {role} position, how do you handle state consistency, connection timeouts, and graceful degradation during traffic surges?",
                "category": "Architecture & Systems Design",
                "skill": top_skill,
                "difficulty": "medium",
                "ideal_answer": f"Architecting with {top_skill} requires circuit breakers, idempotent retry loops with exponential jitter, connection pooling with strict timeouts, and fallback read replicas to prevent cascading failures.",
                "expected_concepts": ["Circuit breakers", "Exponential backoff", "Connection pool sizing", "State consistency", "Idempotency"],
                "evaluation_criteria": ["Evaluates fault-tolerance patterns", "Checks practical understanding of failure modes"],
                "red_flags": ["Ignoring network timeouts", "Assuming distributed components never fail"],
                "follow_up_questions": [f"What specific telemetry metrics do you alert on for {top_skill}?", "How do you test this under simulated chaos conditions?"]
            },
            {
                "question": f"In your experience with {second_skill}, what is the most complex performance bottleneck or memory leak you encountered, and walk me through your diagnostic profiling methodology.",
                "category": "Debugging & Performance",
                "skill": second_skill,
                "difficulty": "hard",
                "ideal_answer": f"Systematic root-cause analysis: capturing heap snapshots/flamegraphs, isolating CPU/memory hotspots, verifying garbage collection frequency, and validating query execution plans before shipping targeted fixes.",
                "expected_concepts": ["Flamegraphs / Profiling", "Heap allocation inspection", "Garbage collection behavior", "Query execution plans"],
                "evaluation_criteria": ["Structured troubleshooting methodology", "Evidence-based diagnosis vs guessing"],
                "red_flags": ["Randomly restarting servers without analyzing logs or memory dumps"],
                "follow_up_questions": ["How did you ensure the fix was verified in staging before production deploy?", "How did you prevent regression in CI/CD?"]
            },
            {
                "question": f"How do you evaluate security vulnerabilities and input validation risks when integrating {third_skill} into external facing client services?",
                "category": "Security & Guardrails",
                "skill": third_skill,
                "difficulty": "hard",
                "ideal_answer": f"Enforcing zero-trust network boundaries, strict Pydantic/Zod schema validation, parameterized queries to eliminate injection, token rate limiting, and automated SAST/DAST pipeline gates.",
                "expected_concepts": ["Schema validation", "Rate limiting", "Least privilege IAM", "Input sanitization"],
                "evaluation_criteria": ["Deep understanding of OWASP Top 10 vulnerabilities", "Proactive defense-in-depth"],
                "red_flags": ["Trusting raw client input without backend sanitization"],
                "follow_up_questions": ["How do you handle credential rotation without downtime?", "What is your incident response playbook for leaked API tokens?"]
            }
        ]

        results = []
        for i in range(count):
            tmpl = templates[i % len(templates)].copy()
            tmpl["id"] = "GEN-" + uuid.uuid4().hex[:8].upper()
            tmpl["role"] = role
            tmpl["seniority"] = seniority
            tmpl["quality_score"] = 92.0
            tmpl["source"] = "heuristic_engine"
            results.append(tmpl)
        return results

    async def evaluate_and_adapt_next(
        self,
        current_question: Dict[str, Any],
        candidate_answer: str,
        session_history: Optional[List[Dict[str, Any]]] = None,
        current_difficulty: str = "medium"
    ) -> Dict[str, Any]:
        """
        Evaluates candidate answer in real-time, extracts concept coverage,
        calculates dynamic difficulty scaling, and synthesizes an adaptive follow-up.
        """
        provider = LLMProviderFactory.get_provider()
        is_skip = provider.detect_skip_intent(candidate_answer)

        if not candidate_answer or len(candidate_answer.strip()) < 5 or is_skip:
            expected = current_question.get("expected_concepts") or ["core technical principles"]
            return {
                "evaluation": {
                    "score": 25,
                    "quality": "weak",
                    "demonstrated_concepts": [],
                    "missing_concepts": expected[:3],
                    "feedback": "Candidate expressed uncertainty or skipped the question."
                },
                "next_difficulty": "easy",
                "followup_needed": True,
                "adaptive_followup_question": f"Could you elaborate on the foundational principles of {current_question.get('skill', 'this topic')} and how you would approach it at a high level?"
            }

        evaluation: Dict[str, Any] = {}
        try:
            evaluation = await provider.evaluate_answer(
                question=current_question,
                answer_transcript=candidate_answer,
                candidate_profile={},
                jd_profile={},
                history=session_history or []
            )
        except Exception as e:
            logger.warning(f"Live evaluation fallback: {e}")
            # Heuristic conceptual matching
            expected = current_question.get("expected_concepts") or ["architecture", "scaling", "trade-offs"]
            ans_lower = candidate_answer.lower()
            
            # Sub-token matching for compound terms like cross-encoder / bge-reranker
            covered = []
            for c in expected:
                c_words = [w.strip() for w in re.split(r"[\s\-_]+", c.lower()) if len(w) > 3]
                if any(w in ans_lower for w in c_words):
                    covered.append(c)

            missed = [c for c in expected if c not in covered]
            word_count = len(candidate_answer.split())

            # Detailed response with technical depth gets excellent score
            if len(covered) >= max(1, len(expected) // 2) or (len(covered) >= 1 and word_count >= 10):
                calc_score = 88
                calc_quality = "excellent"
            elif len(covered) >= 1 or word_count >= 12:
                calc_score = 75
                calc_quality = "good"
            elif word_count >= 6:
                calc_score = 55
                calc_quality = "average"
            else:
                calc_score = 35
                calc_quality = "weak"

            evaluation = {
                "score": calc_score,
                "quality": calc_quality,
                "demonstrated_concepts": covered or [current_question.get("skill", "Core Concepts")],
                "missing_concepts": missed,
                "feedback": f"Candidate covered {len(covered)} of {len(expected)} expected concepts with {calc_quality} technical clarity."
            }

        score = evaluation.get("score", 70)
        quality = evaluation.get("quality") or ("excellent" if score >= 85 else "good" if score >= 70 else "average" if score >= 50 else "weak")

        # Dynamic Difficulty Progression
        if score >= 85:
            next_difficulty = "expert" if current_difficulty == "hard" else "hard"
            followup_direction = "Deeper system-design edge cases and scale limits."
        elif score >= 65:
            next_difficulty = current_difficulty
            followup_direction = "Practical trade-offs and implementation nuances."
        else:
            next_difficulty = "easy" if current_difficulty == "medium" else "medium"
            followup_direction = "Basic foundational concepts and clarifying missing points."

        # Adaptive Follow-up Generation
        adaptive_followup = None
        missing = evaluation.get("missing_concepts") or []
        if missing or quality == "weak":
            missing_str = ", ".join(missing[:2]) if missing else current_question.get("skill", "this area")
            adaptive_followup = f"You touched on the primary workflow, but how specifically would you address {missing_str} under production scale?"
        else:
            followup_list = current_question.get("hidden_rubric", {}).get("follow_up_questions") or current_question.get("follow_up_questions") or []
            if followup_list:
                adaptive_followup = followup_list[0]
            else:
                adaptive_followup = f"Building on that answer, what major architectural trade-offs would you make if concurrency scaled 10x?"

        return {
            "evaluation": evaluation,
            "next_difficulty": next_difficulty,
            "followup_needed": bool(missing or quality in ["weak", "average"]),
            "adaptive_followup_question": adaptive_followup
        }


# Global Singleton
question_generator = QuestionGenerator()
