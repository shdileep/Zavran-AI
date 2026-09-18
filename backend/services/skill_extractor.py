"""
Zavran AI — Multi-source Skill Extraction Engine
Extracts technical skills, frameworks, languages, databases, cloud platforms,
AI/ML concepts, domain skills, and soft skills from Job Descriptions, Resumes, and Roles.
"""

import re
from typing import Dict, Any, List, Set, Optional

# Curated high-precision skill lexicon
SKILL_LEXICON = {
    # AI / ML
    "python": "Python",
    "pytorch": "PyTorch",
    "tensorflow": "TensorFlow",
    "scikit-learn": "Scikit-Learn",
    "sklearn": "Scikit-Learn",
    "rag": "RAG",
    "langchain": "LangChain",
    "langgraph": "LangGraph",
    "llamaindex": "LlamaIndex",
    "llm": "LLM",
    "llms": "LLMs",
    "transformers": "Transformers",
    "huggingface": "Hugging Face",
    "fine-tuning": "Fine-Tuning",
    "vector database": "Vector Databases",
    "pinecone": "Pinecone",
    "qdrant": "Qdrant",
    "weaviate": "Weaviate",
    "chromadb": "ChromaDB",
    "embeddings": "Embeddings",
    "deep learning": "Deep Learning",
    "machine learning": "Machine Learning",
    "nlp": "NLP",
    "computer vision": "Computer Vision",
    "prompt engineering": "Prompt Engineering",
    "agents": "AI Agents",
    "evals": "LLM Evaluation",
    
    # Backend & Languages
    "fastapi": "FastAPI",
    "django": "Django",
    "flask": "Flask",
    "node.js": "Node.js",
    "nodejs": "Node.js",
    "express": "Express.js",
    "nest.js": "NestJS",
    "nestjs": "NestJS",
    "java": "Java",
    "spring boot": "Spring Boot",
    "spring": "Spring Boot",
    "golang": "Go",
    "go": "Go",
    "rust": "Rust",
    "c++": "C++",
    "c#": "C#",
    ".net": ".NET",
    "graphql": "GraphQL",
    "rest": "REST APIs",
    "restful": "REST APIs",
    "grpc": "gRPC",
    "microservices": "Microservices",
    "websockets": "WebSockets",
    "sse": "Server-Sent Events",
    
    # Frontend
    "javascript": "JavaScript",
    "typescript": "TypeScript",
    "react": "React",
    "react.js": "React",
    "next.js": "Next.js",
    "nextjs": "Next.js",
    "vue": "Vue.js",
    "vue.js": "Vue.js",
    "angular": "Angular",
    "redux": "Redux",
    "tailwind": "TailwindCSS",
    "tailwindcss": "TailwindCSS",
    "html": "HTML",
    "css": "CSS",
    
    # Databases & Caching
    "postgresql": "PostgreSQL",
    "postgres": "PostgreSQL",
    "mysql": "MySQL",
    "mongodb": "MongoDB",
    "redis": "Redis",
    "sqlite": "SQLite",
    "cassandra": "Cassandra",
    "dynamodb": "DynamoDB",
    "elasticsearch": "Elasticsearch",
    
    # Cloud & DevOps
    "docker": "Docker",
    "kubernetes": "Kubernetes",
    "k8s": "Kubernetes",
    "aws": "AWS",
    "azure": "Azure",
    "gcp": "GCP",
    "terraform": "Terraform",
    "ci/cd": "CI/CD",
    "linux": "Linux",
    "git": "Git",
    "github actions": "GitHub Actions",
    "prometheus": "Prometheus",
    "grafana": "Grafana",
    
    # Data & Analytics
    "sql": "SQL",
    "pandas": "Pandas",
    "numpy": "NumPy",
    "tableau": "Tableau",
    "powerbi": "PowerBI",
    "power bi": "PowerBI",
    "spark": "Apache Spark",
    "airflow": "Apache Airflow",
    "dbt": "dbt",
    "kafka": "Apache Kafka",
    
    # HR & Product / Soft Skills
    "recruitment": "Recruitment",
    "talent acquisition": "Talent Acquisition",
    "performance management": "Performance Management",
    "conflict resolution": "Conflict Resolution",
    "employee relations": "Employee Relations",
    "product management": "Product Management",
    "agile": "Agile/Scrum",
    "scrum": "Agile/Scrum",
    "system design": "System Design",
    "architecture": "Architecture",
    "leadership": "Leadership",
    "communication": "Communication"
}


class SkillExtractor:
    """
    Fast, deterministic, regex-based and heuristic skill extractor.
    Extracts structured skill groups from text, resumes, and JDs.
    """

    @classmethod
    def extract_skills_from_text(cls, text: Optional[str]) -> List[str]:
        if not text:
            return []

        text_lower = text.lower()
        extracted: Set[str] = set()

        for term, canonical in SKILL_LEXICON.items():
            # Exact word boundary search
            pattern = r"\b" + re.escape(term) + r"\b"
            if re.search(pattern, text_lower):
                extracted.add(canonical)

        return sorted(list(extracted))

    @classmethod
    def extract_from_profiles(
        cls,
        role: str,
        jd_text: Optional[str] = None,
        resume_text: Optional[str] = None,
        explicit_skills: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Combines and attributes skills across Role, JD, Resume, and explicit selections.
        """
        role_skills = cls.extract_skills_from_text(role)
        jd_skills = cls.extract_skills_from_text(jd_text)
        resume_skills = cls.extract_skills_from_text(resume_text)
        explicit = explicit_skills or []

        all_skills = list(dict.fromkeys(explicit + jd_skills + resume_skills + role_skills))

        # Categorize skills
        categories = {
            "ai_ml": [s for s in all_skills if s in ["Python", "PyTorch", "TensorFlow", "RAG", "LangChain", "LLM", "LLMs", "Transformers", "Vector Databases", "Embeddings", "Deep Learning", "Machine Learning", "NLP"]],
            "backend": [s for s in all_skills if s in ["FastAPI", "Django", "Flask", "Node.js", "Java", "Spring Boot", "Go", "Rust", "C#", "GraphQL", "REST APIs", "Microservices"]],
            "frontend": [s for s in all_skills if s in ["React", "TypeScript", "JavaScript", "Next.js", "Vue.js", "Angular", "TailwindCSS", "HTML", "CSS"]],
            "databases": [s for s in all_skills if s in ["PostgreSQL", "MySQL", "MongoDB", "Redis", "SQLite", "DynamoDB", "Elasticsearch"]],
            "cloud_devops": [s for s in all_skills if s in ["Docker", "Kubernetes", "AWS", "Azure", "GCP", "Terraform", "CI/CD", "Linux", "Git"]],
            "soft_skills": [s for s in all_skills if s in ["Communication", "Leadership", "Conflict Resolution", "Agile/Scrum", "Talent Acquisition", "Employee Relations"]]
        }

        return {
            "all_skills": all_skills,
            "jd_skills": jd_skills,
            "resume_skills": resume_skills,
            "role_skills": role_skills,
            "categorized": categories,
        }
