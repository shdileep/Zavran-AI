"""
Zavran AI — Internal Persistent Question Bank & Semantic Deduplication Engine
Manages permanent storage, semantic similarity checking, deduplication, retrieval-first reuse,
and quality scoring for all interview questions in Zavran AI.
"""

import os
import json
import sqlite3
import time
import math
import uuid
import re
import logging
from pathlib import Path
from typing import Dict, Any, List, Optional, Tuple

logger = logging.getLogger("ZavranAI.QuestionBank")

# Persistent DB Path
DB_DIR = Path(__file__).resolve().parent / "data"
DB_DIR.mkdir(parents=True, exist_ok=True)
DB_PATH = DB_DIR / "question_bank.db"

# Similarity threshold for detecting duplicate/redundant questions (configurable)
DEFAULT_SIMILARITY_THRESHOLD = 0.80


def _tokenize(text: str) -> List[str]:
    """Tokenizes and normalizes text for semantic n-gram similarity."""
    if not text:
        return []
    cleaned = re.sub(r"[^\w\s]", " ", text.lower())
    tokens = [w for w in cleaned.split() if len(w) > 2]
    # Add bigrams for structural context
    bigrams = [f"{tokens[i]}_{tokens[i+1]}" for i in range(len(tokens) - 1)]
    return tokens + bigrams


def compute_semantic_similarity(text1: str, text2: str) -> float:
    """
    Computes cosine-weighted Jaccard/TF-IDF similarity between two question texts.
    Returns float score between 0.0 and 1.0.
    """
    tokens1 = _tokenize(text1)
    tokens2 = _tokenize(text2)
    if not tokens1 or not tokens2:
        return 0.0

    set1 = set(tokens1)
    set2 = set(tokens2)
    intersection = set1.intersection(set2)
    union = set1.union(set2)

    if not union:
        return 0.0

    jaccard = len(intersection) / len(union)

    # Term frequency cosine calculation
    tf1 = {t: tokens1.count(t) for t in set1}
    tf2 = {t: tokens2.count(t) for t in set2}

    dot_product = sum(tf1.get(t, 0) * tf2.get(t, 0) for t in intersection)
    mag1 = math.sqrt(sum(v * v for v in tf1.values()))
    mag2 = math.sqrt(sum(v * v for v in tf2.values()))

    cosine = dot_product / (mag1 * mag2) if (mag1 * mag2) > 0 else 0.0
    return 0.6 * cosine + 0.4 * jaccard


class QuestionBank:
    """
    Persistent Question Bank managing schema-validated interview questions,
    deduplication, retrieval-first reuse, and usage tracking.
    """

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(QuestionBank, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, db_path: Path = DB_PATH):
        if self._initialized:
            return
        self.db_path = db_path
        self._init_db()
        self._seed_initial_questions_if_empty()
        self._initialized = True

    def _get_connection(self) -> sqlite3.Connection:
        conn = sqlite3.connect(str(self.db_path))
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA journal_mode=WAL;")
        conn.execute("PRAGMA synchronous=NORMAL;")
        return conn

    def _init_db(self):
        """Initializes the interview_questions table matching specifications."""
        with self._get_connection() as conn:
            conn.execute("""
                CREATE TABLE IF NOT EXISTS interview_questions (
                    id TEXT PRIMARY KEY,
                    role_id TEXT,
                    role TEXT NOT NULL,
                    category TEXT NOT NULL,
                    skill TEXT NOT NULL,
                    question TEXT NOT NULL,
                    ideal_answer TEXT NOT NULL,
                    difficulty TEXT NOT NULL,
                    seniority TEXT NOT NULL,
                    industry TEXT DEFAULT '',
                    job_description_context TEXT DEFAULT '',
                    evaluation_criteria TEXT DEFAULT '[]',
                    expected_concepts TEXT DEFAULT '[]',
                    red_flags TEXT DEFAULT '[]',
                    follow_up_questions TEXT DEFAULT '[]',
                    estimated_time_seconds INTEGER DEFAULT 90,
                    source TEXT DEFAULT 'llm_generated',
                    version INTEGER DEFAULT 1,
                    verified INTEGER DEFAULT 0,
                    usage_count INTEGER DEFAULT 0,
                    quality_score REAL DEFAULT 90.0,
                    normalized_role TEXT DEFAULT '',
                    content_hash TEXT DEFAULT '',
                    dataset_name TEXT DEFAULT '',
                    source_url TEXT DEFAULT '',
                    created_at REAL NOT NULL,
                    updated_at REAL NOT NULL
                );
            """)
            # Safe schema migrations for existing database files
            for col, col_type in [
                ("normalized_role", "TEXT DEFAULT ''"),
                ("content_hash", "TEXT DEFAULT ''"),
                ("dataset_name", "TEXT DEFAULT ''"),
                ("source_url", "TEXT DEFAULT ''"),
            ]:
                try:
                    conn.execute(f"ALTER TABLE interview_questions ADD COLUMN {col} {col_type};")
                except Exception:
                    pass

            conn.execute("CREATE INDEX IF NOT EXISTS idx_iq_role ON interview_questions(role);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_iq_norm_role ON interview_questions(normalized_role);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_iq_category ON interview_questions(category);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_iq_skill ON interview_questions(skill);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_iq_difficulty ON interview_questions(difficulty);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_iq_verified ON interview_questions(verified);")
            conn.execute("CREATE INDEX IF NOT EXISTS idx_iq_source ON interview_questions(source);")
            conn.commit()

    def find_duplicate_or_similar(
        self,
        question_text: str,
        role: Optional[str] = None,
        threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    ) -> Tuple[bool, Optional[Dict[str, Any]], float]:
        """
        Scans existing questions to detect if an identical or highly similar question already exists.
        Returns: (is_duplicate: bool, matched_record: dict, similarity_score: float)
        """
        if not question_text:
            return False, None, 0.0

        with self._get_connection() as conn:
            if role:
                cursor = conn.execute("SELECT * FROM interview_questions WHERE LOWER(role) = LOWER(?)", (role.strip(),))
            else:
                cursor = conn.execute("SELECT * FROM interview_questions")
            rows = cursor.fetchall()

        best_score = 0.0
        best_match = None

        for row in rows:
            existing_q = row["question"]
            sim = compute_semantic_similarity(question_text, existing_q)
            if sim > best_score:
                best_score = sim
                best_match = dict(row)

        is_dup = best_score >= threshold
        return is_dup, best_match, round(best_score, 4)

    def save_question(
        self,
        question_data: Dict[str, Any],
        reject_duplicates: bool = True,
        similarity_threshold: float = DEFAULT_SIMILARITY_THRESHOLD,
    ) -> Dict[str, Any]:
        """
        Validates, deduplicates, and permanently stores a question in the database.
        """
        q_text = (question_data.get("question") or "").strip()
        if not q_text or len(q_text) < 15:
            raise ValueError("Question text must be at least 15 characters long.")

        role = (question_data.get("role") or "General Software Engineer").strip()

        # Check duplicate
        if reject_duplicates:
            is_dup, match, score = self.find_duplicate_or_similar(q_text, role=role, threshold=similarity_threshold)
            if is_dup and match:
                logger.info(f"Question duplicate detected (score: {score}). Reusing existing ID: {match['id']}")
                # Increment existing question usage
                self.record_usage(match["id"])
                return match

        q_id = question_data.get("id") or ("Q-" + uuid.uuid4().hex[:10].upper())
        now = time.time()

        # Prepare JSON fields
        eval_criteria = question_data.get("evaluation_criteria") or []
        if isinstance(eval_criteria, list):
            eval_criteria_str = json.dumps(eval_criteria)
        else:
            eval_criteria_str = str(eval_criteria)

        expected_concepts = question_data.get("expected_concepts") or []
        if isinstance(expected_concepts, list):
            expected_concepts_str = json.dumps(expected_concepts)
        else:
            expected_concepts_str = str(expected_concepts)

        red_flags = question_data.get("red_flags") or []
        if isinstance(red_flags, list):
            red_flags_str = json.dumps(red_flags)
        else:
            red_flags_str = str(red_flags)

        follow_ups = question_data.get("follow_up_questions") or []
        if isinstance(follow_ups, list):
            follow_ups_str = json.dumps(follow_ups)
        else:
            follow_ups_str = str(follow_ups)

        category = (question_data.get("category") or "Technical").strip()
        skill = (question_data.get("skill") or "Engineering").strip()
        ideal_answer = (question_data.get("ideal_answer") or "Demonstrates clear hands-on experience and trade-offs.").strip()
        difficulty = (question_data.get("difficulty") or "medium").lower()
        seniority = (question_data.get("seniority") or "Mid-Level").strip()
        industry = (question_data.get("industry") or "").strip()
        jd_context = (question_data.get("job_description_context") or "").strip()
        est_seconds = int(question_data.get("estimated_time_seconds") or 90)
        source = question_data.get("source") or "llm_generated"
        version = int(question_data.get("version") or 1)
        verified = 1 if question_data.get("verified") else 0
        usage_count = int(question_data.get("usage_count") or 0)
        quality_score = float(question_data.get("quality_score") or 92.0)

        normalized_role = (question_data.get("normalized_role") or role).strip()
        content_hash = (question_data.get("content_hash") or "").strip()
        dataset_name = (question_data.get("dataset_name") or question_data.get("dataset") or "").strip()
        source_url = (question_data.get("source_url") or "").strip()

        with self._get_connection() as conn:
            conn.execute("""
                INSERT OR REPLACE INTO interview_questions (
                    id, role_id, role, category, skill, question, ideal_answer,
                    difficulty, seniority, industry, job_description_context,
                    evaluation_criteria, expected_concepts, red_flags, follow_up_questions,
                    estimated_time_seconds, source, version, verified, usage_count,
                    quality_score, normalized_role, content_hash, dataset_name, source_url,
                    created_at, updated_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                q_id,
                question_data.get("role_id") or ("ROL-" + role[:3].upper()),
                role,
                category,
                skill,
                q_text,
                ideal_answer,
                difficulty,
                seniority,
                industry,
                jd_context,
                eval_criteria_str,
                expected_concepts_str,
                red_flags_str,
                follow_ups_str,
                est_seconds,
                source,
                version,
                verified,
                usage_count,
                quality_score,
                normalized_role,
                content_hash,
                dataset_name,
                source_url,
                now,
                now
            ))
            conn.commit()

        return self.get_question_by_id(q_id)

    def get_question_by_id(self, question_id: str) -> Optional[Dict[str, Any]]:
        with self._get_connection() as conn:
            cursor = conn.execute("SELECT * FROM interview_questions WHERE id = ?", (question_id,))
            row = cursor.fetchone()
            if not row:
                return None
            return self._row_to_dict(row)

    def search_questions(
        self,
        role: Optional[str] = None,
        skills: Optional[List[str]] = None,
        difficulty: Optional[str] = None,
        seniority: Optional[str] = None,
        category: Optional[str] = None,
        query: Optional[str] = None,
        verified_only: bool = False,
        limit: int = 15,
    ) -> List[Dict[str, Any]]:
        """
        Retrieves matching existing questions from the question bank.
        Prioritizes high quality score, verified status, and low usage count.
        """
        clauses = []
        params = []

        if role:
            clauses.append("(LOWER(role) = LOWER(?) OR LOWER(role) LIKE ? OR LOWER(normalized_role) = LOWER(?) OR LOWER(normalized_role) LIKE ?)")
            params.append(role.strip())
            params.append(f"%{role.strip().lower()}%")
            params.append(role.strip())
            params.append(f"%{role.strip().lower()}%")

        if category:
            clauses.append("LOWER(category) = LOWER(?)")
            params.append(category.strip())

        if difficulty:
            clauses.append("LOWER(difficulty) = LOWER(?)")
            params.append(difficulty.strip())

        if seniority and seniority.lower() != "all":
            clauses.append("(LOWER(seniority) = LOWER(?) OR LOWER(seniority) = 'all')")
            params.append(seniority.strip())

        if verified_only:
            clauses.append("verified = 1")

        if query:
            q_clean = f"%{query.strip().lower()}%"
            clauses.append("(LOWER(question) LIKE ? OR LOWER(skill) LIKE ? OR LOWER(expected_concepts) LIKE ?)")
            params.extend([q_clean, q_clean, q_clean])

        where_str = " AND ".join(clauses) if clauses else "1=1"
        sql = f"""
            SELECT * FROM interview_questions
            WHERE {where_str}
            ORDER BY quality_score DESC, verified DESC, usage_count ASC
            LIMIT ?
        """
        params.append(limit * 2)

        with self._get_connection() as conn:
            cursor = conn.execute(sql, params)
            rows = cursor.fetchall()

        results = [self._row_to_dict(r) for r in rows]

        # Skill re-ranking if specific skills were provided
        if skills and results:
            skills_lower = [s.strip().lower() for s in skills if s.strip()]
            def skill_match_weight(item: Dict[str, Any]) -> int:
                count = 0
                item_skill = item.get("skill", "").lower()
                concepts = [c.lower() for c in item.get("expected_concepts", [])]
                for sk in skills_lower:
                    if sk in item_skill or any(sk in c for c in concepts):
                        count += 3
                return count

            results.sort(key=lambda x: (skill_match_weight(x), x["quality_score"], -x["usage_count"]), reverse=True)

        return results[:limit]

    def record_usage(self, question_id: str):
        """Increments usage count for a question."""
        with self._get_connection() as conn:
            conn.execute(
                "UPDATE interview_questions SET usage_count = usage_count + 1, updated_at = ? WHERE id = ?",
                (time.time(), question_id),
            )
            conn.commit()

    def record_feedback(self, question_id: str, candidate_score: float):
        """
        Updates quality score dynamically based on candidate performance and evaluation outcome.
        """
        with self._get_connection() as conn:
            conn.execute(
                """UPDATE interview_questions
                   SET quality_score = (quality_score * 0.9) + (? * 0.1),
                       updated_at = ?
                   WHERE id = ?""",
                (float(candidate_score), time.time(), question_id),
            )
            conn.commit()

    def update_question(self, question_id: str, updates: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Admin helper to edit a question."""
        existing = self.get_question_by_id(question_id)
        if not existing:
            return None

        for k, v in updates.items():
            existing[k] = v
        existing["updated_at"] = time.time()
        existing["version"] = existing.get("version", 1) + 1

        return self.save_question(existing, reject_duplicates=False)

    def delete_question(self, question_id: str) -> bool:
        """Admin helper to delete a question."""
        with self._get_connection() as conn:
            cursor = conn.execute("DELETE FROM interview_questions WHERE id = ?", (question_id,))
            conn.commit()
            return cursor.rowcount > 0

    def verify_question(self, question_id: str, verified: bool = True) -> bool:
        """Admin helper to mark question as verified."""
        with self._get_connection() as conn:
            cursor = conn.execute(
                "UPDATE interview_questions SET verified = ?, updated_at = ? WHERE id = ?",
                (1 if verified else 0, time.time(), question_id),
            )
            conn.commit()
            return cursor.rowcount > 0

    def get_stats(self) -> Dict[str, Any]:
        """Returns question bank metrics and category breakdowns."""
        with self._get_connection() as conn:
            total = conn.execute("SELECT COUNT(*) FROM interview_questions").fetchone()[0]
            verified = conn.execute("SELECT COUNT(*) FROM interview_questions WHERE verified = 1").fetchone()[0]
            avg_score = conn.execute("SELECT AVG(quality_score) FROM interview_questions").fetchone()[0] or 0.0
            total_usage = conn.execute("SELECT SUM(usage_count) FROM interview_questions").fetchone()[0] or 0

            cat_rows = conn.execute("SELECT category, COUNT(*) as cnt FROM interview_questions GROUP BY category").fetchall()
            cat_breakdown = {r["category"]: r["cnt"] for r in cat_rows}

            role_rows = conn.execute("SELECT COUNT(DISTINCT role) FROM interview_questions").fetchone()[0]

        return {
            "total_questions": total,
            "verified_questions": verified,
            "distinct_roles_covered": role_rows,
            "average_quality_score": round(avg_score, 1),
            "total_usage_count": total_usage,
            "categories": cat_breakdown,
        }

    def _row_to_dict(self, row: sqlite3.Row) -> Dict[str, Any]:
        d = dict(row)
        for json_field in ["evaluation_criteria", "expected_concepts", "red_flags", "follow_up_questions"]:
            if json_field in d and isinstance(d[json_field], str):
                try:
                    d[json_field] = json.loads(d[json_field])
                except Exception:
                    d[json_field] = []
        d["verified"] = bool(d.get("verified"))
        return d

    def _seed_initial_questions_if_empty(self):
        """Populates the database with initial verified questions for core roles."""
        logger.info("Verifying initial high-quality validated question bank...")
        seed_questions = [
            # AI Engineer
            {
                "id": "SEED-AI-01",
                "role": "AI Engineer",
                "category": "Architecture & Systems Design",
                "skill": "RAG & Vector Search",
                "difficulty": "medium",
                "seniority": "Senior",
                "question": "Walk me through how you architect low-latency AI pipelines with streaming responses while maintaining context window efficiency and vector search precision.",
                "ideal_answer": "A resilient streaming RAG architecture uses asynchronous SSE/WebSockets, semantic chunking (256-512 tokens with 10% overlap), approximate nearest neighbor indexing (HNSW), dynamic reranking with cross-encoders, and tiered prompt caching to keep TTFT under 350ms.",
                "evaluation_criteria": ["Mentions streaming SSE/WebSockets", "Discusses chunking and indexing algorithms", "Articulates context window pruning and TTFT trade-offs"],
                "expected_concepts": ["Streaming SSE/WebSockets", "Semantic chunking", "HNSW vector indexing", "Cross-encoder reranking", "TTFT optimization"],
                "red_flags": ["Buffering entire LLM output before transmitting", "Ignoring context window token limits", "Proposing linear O(N) cosine scans over millions of vectors"],
                "follow_up_questions": [
                    "How do you benchmark and reduce First Token Latency (TTFT) when using heavy cross-encoders?",
                    "What strategies prevent stale embeddings when source knowledge bases update continuously?"
                ],
                "verified": 1,
                "quality_score": 96.0,
                "source": "seed"
            },
            {
                "id": "SEED-AI-02",
                "role": "AI Engineer",
                "category": "Guardrails & Safety",
                "skill": "Hallucination Mitigation",
                "difficulty": "hard",
                "seniority": "Staff",
                "question": "How do you systematically mitigate hallucinations and prompt injections in autonomous tool-calling production agents?",
                "ideal_answer": "Multi-layered defense: strict Pydantic/Zod structured output schema validation, dual-LLM evaluator patterns (canary checks), least-privilege sandboxed tool execution with idempotency tokens, and real-time guardrail classifiers (NeMo/Llama Guard).",
                "evaluation_criteria": ["Explains schema enforcement loops", "Details least-privilege tool execution sandbox", "Addresses prompt injection canary tokens"],
                "expected_concepts": ["Structured output schemas", "Sandboxed tool execution", "Dual-LLM guardrail evaluators", "Canary tokens & input sanitization"],
                "red_flags": ["Relying purely on system prompt admonitions without runtime validation", "Allowing raw arbitrary code execution without isolation"],
                "follow_up_questions": [
                    "How do you handle tool execution rollbacks if a multi-step agent fails on step 4 of 5?",
                    "How do you prevent indirect prompt injection from retrieved external web content?"
                ],
                "verified": 1,
                "quality_score": 97.0,
                "source": "seed"
            },
            # Backend Developer
            {
                "id": "SEED-BE-01",
                "role": "Backend Developer",
                "category": "Concurrency & Database",
                "skill": "Connection Pooling & State",
                "difficulty": "hard",
                "seniority": "Senior",
                "question": "Under high concurrency (10,000+ RPS), how do you manage database connection pool sizing, transaction isolation levels, and prevent connection starvation in FastAPI/Go microservices?",
                "ideal_answer": "Sizing pool size using Little's Law based on query duration and CPU cores, offloading pooling to PgBouncer, setting strict statement timeouts (e.g. 500ms), using READ COMMITTED with optimistic concurrency control (OCC) or advisory locks where appropriate to prevent deadlocks.",
                "evaluation_criteria": ["Explains connection pool math and PgBouncer integration", "Differentiates transaction isolation levels", "Details statement timeouts and connection leak prevention"],
                "expected_concepts": ["PgBouncer connection pooling", "Statement timeout budgets", "Optimistic concurrency control", "Deadlock detection", "Asynchronous I/O loop non-blocking behavior"],
                "red_flags": ["Setting pool size to 10,000 threads directly on Postgres", "Holding open transactions across external HTTP network calls"],
                "follow_up_questions": [
                    "What happens when downstream database latency spikes from 5ms to 200ms under full load?",
                    "How do you implement distributed locking across stateless worker pods?"
                ],
                "verified": 1,
                "quality_score": 95.0,
                "source": "seed"
            },
            # Full Stack Engineer
            {
                "id": "SEED-FS-01",
                "role": "Full Stack Engineer",
                "category": "State & Performance",
                "skill": "Full Stack Architecture",
                "difficulty": "medium",
                "seniority": "Mid-Level",
                "question": "How do you coordinate real-time state synchronization between a Next.js/React frontend and a WebSocket backend while handling reconnections and packet loss gracefully?",
                "ideal_answer": "Using an optimistic UI update model paired with sequence-numbered server events, heartbeat ping/pong detection, exponential backoff reconnection loops, and a reconciliation queue that replays unacknowledged mutations upon re-establishment.",
                "evaluation_criteria": ["Explains sequence numbering and idempotency", "Covers exponential backoff and heartbeats", "Handles state reconciliation without full page reload"],
                "expected_concepts": ["Sequence numbering", "Heartbeat ping/pong", "Exponential backoff", "Optimistic state rollbacks", "Idempotency keys"],
                "red_flags": ["Polling aggressively on socket disconnect", "Assuming TCP guarantees socket-level application state recovery without sequence tracking"],
                "follow_up_questions": [
                    "How do you prevent duplicate message rendering if a reconnection happens mid-flight?",
                    "How do you manage memory footprint in the browser during 8-hour continuous streaming sessions?"
                ],
                "verified": 1,
                "quality_score": 94.0,
                "source": "seed"
            },
            # Data Scientist
            {
                "id": "SEED-DS-01",
                "role": "Data Scientist",
                "category": "Model Evaluation & Drift",
                "skill": "Statistical Modeling",
                "difficulty": "medium",
                "seniority": "Senior",
                "question": "When deploying a classification model into production, how do you distinguish between covariate shift, concept drift, and label shift, and what is your monitoring playbook for each?",
                "ideal_answer": "Covariate shift (P(X) changes): detected via PSI (Population Stability Index) or KS tests on features without labels. Concept drift (P(Y|X) changes): monitored via performance decay against delayed ground truth labels. Label shift (P(Y) changes): tracked through prior class distribution shifts. Playbook includes automated retraining triggers and feature importance drift alerts.",
                "evaluation_criteria": ["Clearly distinguishes P(X), P(Y|X), and P(Y) distributions", "Specifies statistical tests like PSI and KS-test", "Details automated remediation workflows"],
                "expected_concepts": ["Covariate shift vs Concept drift vs Prior shift", "Population Stability Index (PSI)", "Kolmogorov-Smirnov test", "Delayed ground truth reconciliation", "Shadow model evaluation"],
                "red_flags": ["Confusing feature drift with concept drift", "Relying solely on accuracy without tracking class balance"],
                "follow_up_questions": [
                    "How do you handle retraining when ground truth labels take 60 days to arrive?",
                    "How do you calibrate confidence thresholds under extreme class imbalance (1:10,000)?"
                ],
                "verified": 1,
                "quality_score": 95.0,
                "source": "seed"
            },
            # Product Manager
            {
                "id": "SEED-PM-01",
                "role": "Product Manager",
                "category": "Product Strategy & Trade-offs",
                "skill": "Feature Prioritization",
                "difficulty": "medium",
                "seniority": "Senior",
                "question": "Walk me through how you evaluate trade-offs when enterprise engineering leadership requests a 2-month tech-debt refactor while sales leadership demands immediate custom features to close a $5M deal.",
                "ideal_answer": "Frame tech debt as financial interest: quantify the cost of inaction (incident SLAs, developer velocity decay, churn risk) against the revenue potential and customer contract commitments. Formulate a blended roadmap (e.g. 70% customer features, 30% architectural hardening) or negotiate phased enterprise delivery with decoupled modularity.",
                "evaluation_criteria": ["Quantifies risk and ROI objectively", "Demonstrates empathy for both engineering velocity and commercial urgency", "Creates structured compromise framework"],
                "expected_concepts": ["Opportunity cost quantification", "Tech debt interest modeling", "Blended capacity allocation", "Executive alignment & expectation setting", "Contract SLA protection"],
                "red_flags": ["Blindly siding with sales and ignoring systemic collapse", "Dismissing commercial viability entirely without executive compromise"],
                "follow_up_questions": [
                    "What specific metrics do you present to the executive board to justify architectural refactoring?",
                    "How do you communicate delivery delays to the $5M enterprise prospect without killing the deal?"
                ],
                "verified": 1,
                "quality_score": 93.0,
                "source": "seed"
            },
            # Data Analyst
            {
                "id": "SEED-DA-01",
                "role": "Data Analyst",
                "category": "SQL & Analytics",
                "skill": "SQL Optimization",
                "difficulty": "medium",
                "seniority": "Mid-Level",
                "question": "How do you optimize a slow-running SQL query involving multi-table joins, subqueries, and window functions on a 100M-row table?",
                "ideal_answer": "Analyze the EXPLAIN ANALYZE execution plan to identify sequential scans, missing composite indexes, high-cost hash joins, or Cartesian products. Replace correlated subqueries with CTEs or window functions, prune unnecessary columns, and leverage table partitioning or materialized views for repeated aggregations.",
                "evaluation_criteria": ["Mentions EXPLAIN ANALYZE and execution plans", "Covers indexing strategies and partitioning", "Discusses CTEs vs subquery optimization"],
                "expected_concepts": ["EXPLAIN ANALYZE", "Index scans vs sequential scans", "Composite indexes", "Partitioning", "Window functions"],
                "red_flags": ["Adding indexes blindly on all columns", "Ignoring execution plans"],
                "follow_up_questions": ["When would you prefer a materialized view over a regular view with indexes?"],
                "verified": 1,
                "quality_score": 94.0,
                "source": "seed"
            },
            # HR Manager
            {
                "id": "SEED-HR-01",
                "role": "HR Manager",
                "category": "Conflict Resolution",
                "skill": "Employee Relations",
                "difficulty": "medium",
                "seniority": "Senior",
                "question": "How do you handle a high-stakes performance dispute between a senior engineering manager and a key individual contributor while ensuring fairness and compliance?",
                "ideal_answer": "Conduct independent structured discovery sessions with both parties, review objective objective performance artifacts (PR reviews, deliverables, feedback history), identify root causes (communication vs technical vs workload), establish measurable 30-day alignment goals, and document all outcomes in accordance with labor compliance and company policy.",
                "evaluation_criteria": ["Maintains objective neutrality", "Gathers documented evidence before making decisions", "Aligns with compliance and empathy"],
                "expected_concepts": ["Objective performance metrics", "Structured discovery", "Performance improvement plans", "Labor compliance", "Mediation"],
                "red_flags": ["Taking sides without documentation", "Ignoring retaliation risks"],
                "follow_up_questions": ["What steps do you take if one party threatens legal action or harassment claims?"],
                "verified": 1,
                "quality_score": 95.0,
                "source": "seed"
            }
        ]

        for q in seed_questions:
            self.save_question(q, reject_duplicates=False)
        logger.info(f"Seeded {len(seed_questions)} initial validated questions.")


# Global Singleton
question_bank = QuestionBank()
