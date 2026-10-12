import os
import sys
import time
import asyncio

# Ensure project root is in sys.path
sys.path.insert(0, r"D:\Zevaran")

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

from backend.services.bank_rag_engine import bank_rag_service

async def run_benchmark():
    print("=== BANK RAG BENCHMARK & MULTI-AGENT PIPELINE (6 DOCUMENTS) ===")
    
    # Force re-index with HR PDF.pdf
    print("\n--- Re-indexing all 6 Bank files (pdf1 - pdf5 + HR PDF.pdf) ---")
    stats = bank_rag_service.reindex_bank_documents()
    print(f"Re-indexing Complete in {stats['indexing_time_seconds']}s: Total Chunks = {stats['total_chunks']}, Dimensions = {stats['vector_dimension']}")

    # 1. Test Sub-Millisecond Retrieval across Technical + Behavioral & HR categories
    test_queries = [
        ("Cloud Solutions Architect", "Designing resilient multi-region AWS architectures with Terraform, high availability, and auto-scaling"),
        ("DevOps / SRE Engineer", "Kubernetes pod crashes, CI/CD pipeline failure, prometheus alert storm"),
        ("AI / ML Engineer", "Fine-tuning LLMs with LoRA, vector embeddings, low latency model inference"),
        ("Behavioral & Leadership", "How do you handle conflict with a team member when under tight project deadlines?"),
        ("HR & Culture Fit", "Tell me about yourself beyond your resume and what motivates you at work"),
        ("Ethics & Integrity", "Describe a time when you had to make a tough ethical decision at work")
    ]

    print("\n--- Testing Sub-Millisecond Vector Retrieval (Technical + HR PDF) ---")
    for role_or_cat, query in test_queries:
        res = bank_rag_service.query(query_text=query, target_role=role_or_cat, top_k=3)
        print(f"\nQuery/Role: {role_or_cat}")
        print(f"  Retrieval Latency: {res['latency_ms']:.3f} ms")
        print(f"  Retrieved Chunks: {res['count']}")
        if res['results']:
            top_hit = res['results'][0]
            print(f"  Top Match [{top_hit.get('doc_name')} | Page {top_hit.get('page')} | Category: {top_hit.get('category')}]:")
            print(f"    Q: {top_hit.get('question')[:120]}...")
            print(f"    Score: {top_hit.get('similarity_score')}")

    # 2. Test Full Groq LLM Synthesis with Candidate Resume
    sample_resume = """
    Jane Doe - Lead AI Systems Engineer
    Experience:
    - Led cross-functional team of 8 engineers building enterprise LLM agent workflows and low-latency RAG systems.
    - Mentored junior engineers, resolved cross-team conflicts, and aligned engineering milestones with executive roadmap.
    - Designed vector search indexing with PyMuPDF document extraction and sentence-transformers.
    Skills: Python, PyTorch, PyMuPDF, Groq, FastEmbed, Docker, Kubernetes, Leadership, Teamwork, Conflict Resolution.
    """
    
    print("\n--- Testing Candidate Calibration Pipeline (PyMuPDF + T5 Vector Search + Groq Agent) ---")
    calib = await bank_rag_service.calibrate_candidate(
        resume_text=sample_resume,
        target_role="Lead AI Systems Engineer",
        jd_text="Looking for a technical lead to architect RAG pipelines and mentor the engineering team.",
        question_count=5
    )
    print(f"Calibration Complete!")
    print(f"  Retrieval Latency: {calib['retrieval_latency_ms']:.3f} ms")
    print(f"  Total End-to-End Latency: {calib['total_latency_ms']:.2f} ms")
    print(f"  Total Questions Synthesized: {calib['question_count']}")
    print(f"  Sources: {', '.join(calib.get('sources', []))}")
    for i, q in enumerate(calib['questions'][:4]):
        print(f"\n  [Q{i+1}] {q.get('step_label', '')}")
        print(f"      Question: {q.get('question')}")
        print(f"      Provenance: {q.get('source_provenance', 'Bank')}")
        print(f"      Ideal Answer: {q.get('ideal_answer', '')[:120]}...")

if __name__ == "__main__":
    asyncio.run(run_benchmark())
