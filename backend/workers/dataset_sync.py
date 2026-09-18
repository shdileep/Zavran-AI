"""
Zavran AI — Background Hugging Face Dataset Synchronization Worker
Synchronizes public Hugging Face dataset (Ankshi/hr-interview-dataset) into
Zavran's persistent question bank with batching, deduplication, and cache invalidation.
"""

import time
import logging
import asyncio
from typing import Dict, Any, Optional

from backend.services.dataset_ingestion import DatasetIngestionService
from backend.services.question_cache import question_cache
from backend.question_bank import question_bank

logger = logging.getLogger("ZavranAI.DatasetSyncWorker")


class DatasetSyncWorker:
    """
    Background synchronization worker for Hugging Face Ankshi/hr-interview-dataset.
    """

    def __init__(self, batch_size: int = 100, max_sync_rows: int = 1000):
        self.ingestion_service = DatasetIngestionService()
        self.bank = question_bank
        self.cache = question_cache
        self.batch_size = batch_size
        self.max_sync_rows = max_sync_rows
        self.last_sync_time: Optional[float] = None
        self.sync_stats: Dict[str, Any] = {
            "status": "idle",
            "total_fetched": 0,
            "total_ingested": 0,
            "total_rejected": 0,
            "total_duplicates": 0,
            "errors": 0,
        }

    async def run_sync(self, limit: Optional[int] = None) -> Dict[str, Any]:
        """
        Executes a synchronization cycle from Hugging Face Dataset Server API.
        """
        sync_limit = limit or self.max_sync_rows
        logger.info(f"Starting Hugging Face dataset sync (target: {sync_limit} rows)...")
        
        self.sync_stats["status"] = "in_progress"
        self.sync_stats["started_at"] = time.time()
        
        offset = 0
        fetched_count = 0
        ingested_count = 0
        rejected_count = 0
        duplicate_count = 0
        error_count = 0

        while fetched_count < sync_limit:
            current_length = min(self.batch_size, sync_limit - fetched_count)
            try:
                normalized_batch = await self.ingestion_service.fetch_and_normalize_batch(
                    offset=offset,
                    length=current_length,
                )
                if not normalized_batch:
                    logger.info(f"No further records returned at offset {offset}. Sync complete.")
                    break

                for nq in normalized_batch:
                    try:
                        # Save to question bank with deduplication check
                        existing_match = self.bank.find_duplicate_or_similar(
                            question_text=nq.question,
                            role=nq.role,
                            threshold=0.85
                        )
                        is_dup, match, sim_score = existing_match
                        if is_dup and match:
                            duplicate_count += 1
                            continue

                        # Save question record
                        self.bank.save_question({
                            "id": nq.id,
                            "role_id": "HF-" + nq.normalized_role[:3].upper(),
                            "role": nq.role,
                            "normalized_role": nq.normalized_role,
                            "category": nq.category,
                            "skill": nq.skills[0] if nq.skills else "Engineering",
                            "question": nq.question,
                            "ideal_answer": nq.answer,
                            "difficulty": nq.difficulty.lower(),
                            "seniority": nq.metadata.get("experience", "all"),
                            "source": nq.source,
                            "version": nq.dataset_version,
                            "verified": 1,
                            "quality_score": nq.quality_score,
                            "expected_concepts": nq.skills,
                            "evaluation_criteria": [f"Evaluates depth in {nq.category} and practical reasoning."],
                        }, reject_duplicates=False)
                        ingested_count += 1
                    except Exception as row_err:
                        logger.debug(f"Error storing question {nq.id}: {row_err}")
                        error_count += 1

                fetched_count += len(normalized_batch)
                offset += current_length

            except Exception as e:
                logger.error(f"Error during batch sync at offset {offset}: {e}")
                error_count += 1
                break

        self.last_sync_time = time.time()
        self.sync_stats = {
            "status": "completed",
            "completed_at": self.last_sync_time,
            "total_fetched": fetched_count,
            "total_ingested": ingested_count,
            "total_duplicates": duplicate_count,
            "total_rejected": rejected_count,
            "errors": error_count,
        }

        # Invalidate question cache to ensure fresh questions are retrieved
        self.cache.invalidate()
        logger.info(f"Dataset sync finished: {self.sync_stats}")
        return self.sync_stats


dataset_sync_worker = DatasetSyncWorker()
