"""
Zavran AI — Canonical Role Normalization Engine
Maps arbitrary job titles, JD titles, and resume roles into standardized canonical roles,
aliases, taxonomy families, and default core skills.
"""

import re
from typing import Dict, Any, List, Optional, Tuple


ROLE_TAXONOMY: Dict[str, Dict[str, Any]] = {
    "AI Engineer": {
        "canonical_role": "AI Engineer",
        "category": "AI & Machine Learning",
        "aliases": [
            "ai engineer", "artificial intelligence engineer", "genai engineer",
            "generative ai engineer", "applied ai engineer", "llm engineer",
            "rag engineer", "prompt engineer", "ai research engineer", "ai developer",
            "full stack ai engineer", "ai solutions engineer", "agentic ai engineer"
        ],
        "core_skills": ["Python", "PyTorch", "LLM", "RAG", "LangChain", "FastAPI", "Vector Databases", "Transformers"],
        "category_distribution": {
            "Technical": 30,
            "Role-specific": 15,
            "Project/Experience": 15,
            "Problem solving": 10,
            "Situational": 10,
            "Behavioral": 10,
            "System design": 5,
            "Coding/Practical": 5
        }
    },
    "Machine Learning Engineer": {
        "canonical_role": "Machine Learning Engineer",
        "category": "AI & Machine Learning",
        "aliases": [
            "machine learning engineer", "ml engineer", "deep learning engineer",
            "mlops engineer", "nlp engineer", "computer vision engineer", "applied scientist"
        ],
        "core_skills": ["Python", "PyTorch", "TensorFlow", "Scikit-Learn", "MLflow", "Docker", "Feature Engineering"],
        "category_distribution": {
            "Technical": 30,
            "Role-specific": 15,
            "Project/Experience": 15,
            "Problem solving": 10,
            "Situational": 10,
            "Behavioral": 10,
            "System design": 5,
            "Coding/Practical": 5
        }
    },
    "Backend Engineer": {
        "canonical_role": "Backend Engineer",
        "category": "Software Engineering",
        "aliases": [
            "backend engineer", "backend developer", "back end developer", "server side developer",
            "api engineer", "python developer", "django developer", "fastapi developer",
            "java backend developer", "golang developer", "go developer", "node.js developer",
            "nodejs engineer", "c# .net developer", "spring boot developer"
        ],
        "core_skills": ["Python", "Java", "Go", "Node.js", "PostgreSQL", "Redis", "REST", "GraphQL", "Microservices", "Docker"],
        "category_distribution": {
            "Technical": 30,
            "Role-specific": 15,
            "Project/Experience": 15,
            "Problem solving": 10,
            "Situational": 10,
            "Behavioral": 10,
            "System design": 5,
            "Coding/Practical": 5
        }
    },
    "Frontend Engineer": {
        "canonical_role": "Frontend Engineer",
        "category": "Software Engineering",
        "aliases": [
            "frontend engineer", "frontend developer", "front end developer", "ui developer",
            "react developer", "next.js developer", "vue developer", "angular developer",
            "web developer", "client side engineer"
        ],
        "core_skills": ["React", "TypeScript", "JavaScript", "HTML/CSS", "Next.js", "Redux", "TailwindCSS", "Web Performance"],
        "category_distribution": {
            "Technical": 30,
            "Role-specific": 15,
            "Project/Experience": 15,
            "Problem solving": 10,
            "Situational": 10,
            "Behavioral": 10,
            "System design": 5,
            "Coding/Practical": 5
        }
    },
    "Full Stack Engineer": {
        "canonical_role": "Full Stack Engineer",
        "category": "Software Engineering",
        "aliases": [
            "full stack engineer", "full stack developer", "fullstack engineer",
            "fullstack developer", "software engineer", "software developer", "sde"
        ],
        "core_skills": ["JavaScript", "TypeScript", "Python", "React", "Node.js", "PostgreSQL", "REST APIs", "Docker", "Git"],
        "category_distribution": {
            "Technical": 30,
            "Role-specific": 15,
            "Project/Experience": 15,
            "Problem solving": 10,
            "Situational": 10,
            "Behavioral": 10,
            "System design": 5,
            "Coding/Practical": 5
        }
    },
    "DevOps Engineer": {
        "canonical_role": "DevOps Engineer",
        "category": "Infrastructure & Cloud",
        "aliases": [
            "devops engineer", "site reliability engineer", "sre", "cloud engineer",
            "infrastructure engineer", "platform engineer", "kubernetes engineer",
            "aws cloud architect", "cloud operations engineer"
        ],
        "core_skills": ["Docker", "Kubernetes", "AWS", "Terraform", "CI/CD", "Linux", "Prometheus", "Ansible"],
        "category_distribution": {
            "Technical": 30,
            "Role-specific": 15,
            "Project/Experience": 15,
            "Problem solving": 10,
            "Situational": 10,
            "Behavioral": 10,
            "System design": 5,
            "Coding/Practical": 5
        }
    },
    "Data Analyst": {
        "canonical_role": "Data Analyst",
        "category": "Data & Analytics",
        "aliases": [
            "data analyst", "business intelligence analyst", "bi analyst", "analytics specialist",
            "quantitative analyst", "sql analyst", "data visualization specialist", "reporting analyst"
        ],
        "core_skills": ["SQL", "Excel", "Tableau", "PowerBI", "Python", "Data Visualization", "Statistics", "ETL"],
        "category_distribution": {
            "Technical": 25,
            "Role-specific": 20,
            "Project/Experience": 15,
            "Problem solving": 15,
            "Situational": 10,
            "Behavioral": 10,
            "System design": 0,
            "Coding/Practical": 5
        }
    },
    "Data Scientist": {
        "canonical_role": "Data Scientist",
        "category": "Data & Analytics",
        "aliases": [
            "data scientist", "senior data scientist", "lead data scientist",
            "statistician", "decision scientist", "ai data scientist"
        ],
        "core_skills": ["Python", "R", "SQL", "Machine Learning", "Pandas", "Hypothesis Testing", "Deep Learning", "Data Mining"],
        "category_distribution": {
            "Technical": 30,
            "Role-specific": 15,
            "Project/Experience": 15,
            "Problem solving": 10,
            "Situational": 10,
            "Behavioral": 10,
            "System design": 5,
            "Coding/Practical": 5
        }
    },
    "Product Manager": {
        "canonical_role": "Product Manager",
        "category": "Product & Management",
        "aliases": [
            "product manager", "technical product manager", "product owner",
            "associate product manager", "lead product manager", "pm", "tpm"
        ],
        "core_skills": ["Product Strategy", "Roadmapping", "User Research", "Agile/Scrum", "A/B Testing", "Metrics/KPIs", "Stakeholder Management"],
        "category_distribution": {
            "Technical": 10,
            "Role-specific": 25,
            "Project/Experience": 20,
            "Problem solving": 15,
            "Situational": 15,
            "Behavioral": 15,
            "System design": 0,
            "Coding/Practical": 0
        }
    },
    "HR Manager": {
        "canonical_role": "HR Manager",
        "category": "Human Resources",
        "aliases": [
            "hr manager", "human resources manager", "hr generalist", "hr business partner",
            "hrbp", "talent acquisition specialist", "recruiter", "people operations manager",
            "people partner", "head of people"
        ],
        "core_skills": ["Talent Acquisition", "Employee Relations", "Performance Management", "Conflict Resolution", "HR Compliance", "Culture & Retention", "Onboarding"],
        "category_distribution": {
            "Technical": 5,
            "Role-specific": 30,
            "Project/Experience": 20,
            "Problem solving": 15,
            "Situational": 15,
            "Behavioral": 15,
            "System design": 0,
            "Coding/Practical": 0
        }
    },
    "QA Engineer": {
        "canonical_role": "QA Engineer",
        "category": "Software Engineering",
        "aliases": [
            "qa engineer", "sdet", "quality assurance engineer", "software test engineer",
            "automation engineer", "test automation engineer", "qa analyst"
        ],
        "core_skills": ["Selenium", "Playwright", "PyTest", "Cypress", "API Testing", "Postman", "CI/CD", "Test Planning"],
        "category_distribution": {
            "Technical": 30,
            "Role-specific": 15,
            "Project/Experience": 15,
            "Problem solving": 10,
            "Situational": 10,
            "Behavioral": 10,
            "System design": 5,
            "Coding/Practical": 5
        }
    },
    "Security Engineer": {
        "canonical_role": "Security Engineer",
        "category": "Security & Compliance",
        "aliases": [
            "security engineer", "cybersecurity engineer", "infosec engineer",
            "application security engineer", "appsec engineer", "cloud security engineer",
            "soc analyst", "penetration tester"
        ],
        "core_skills": ["OWASP", "Vulnerability Management", "Cryptography", "Network Security", "IAM", "Incident Response", "SIEM"],
        "category_distribution": {
            "Technical": 30,
            "Role-specific": 15,
            "Project/Experience": 15,
            "Problem solving": 10,
            "Situational": 10,
            "Behavioral": 10,
            "System design": 5,
            "Coding/Practical": 5
        }
    }
}


class RoleNormalizer:
    """
    Normalizes candidate role titles into canonical forms and resolves conflicts
    across Explicit Target Role, Job Description Role, and Resume Inferred Role.
    """

    @classmethod
    def normalize_role(cls, raw_role: Optional[str]) -> str:
        """
        Maps raw input role string into a canonical role name.
        Uses exact alias match, then substring/regex match, then defaults gracefully.
        """
        if not raw_role:
            return "Software Engineer"

        cleaned = raw_role.strip().lower()
        cleaned = re.sub(r"[^\w\s-]", " ", cleaned)
        cleaned = re.sub(r"\s+", " ", cleaned).strip()

        # Direct alias check
        for canonical, data in ROLE_TAXONOMY.items():
            if cleaned == canonical.lower():
                return canonical
            for alias in data["aliases"]:
                if cleaned == alias.lower():
                    return canonical

        # Substring / keyword matches with priority order
        if "genai" in cleaned or "generative ai" in cleaned or "llm" in cleaned or ("ai" in cleaned.split() and "engineer" in cleaned):
            return "AI Engineer"
        if "machine learning" in cleaned or "ml" in cleaned.split() or "deep learning" in cleaned:
            return "Machine Learning Engineer"
        if "backend" in cleaned or "back-end" in cleaned or "back end" in cleaned or "server" in cleaned:
            return "Backend Engineer"
        if "frontend" in cleaned or "front-end" in cleaned or "front end" in cleaned or "react" in cleaned or "ui" in cleaned.split():
            return "Frontend Engineer"
        if "full stack" in cleaned or "fullstack" in cleaned or "full-stack" in cleaned:
            return "Full Stack Engineer"
        if "devops" in cleaned or "sre" in cleaned.split() or "reliability" in cleaned or "infrastructure" in cleaned or "platform" in cleaned:
            return "DevOps Engineer"
        if "data analyst" in cleaned or "business intelligence" in cleaned or "bi analyst" in cleaned:
            return "Data Analyst"
        if "data scientist" in cleaned or "statistician" in cleaned:
            return "Data Scientist"
        if "product manager" in cleaned or "product owner" in cleaned or "tpm" in cleaned.split() or "pm" in cleaned.split():
            return "Product Manager"
        if "hr" in cleaned.split() or "human resources" in cleaned or "talent" in cleaned or "recruiter" in cleaned or "people ops" in cleaned:
            return "HR Manager"
        if "qa" in cleaned.split() or "sdet" in cleaned.split() or "test" in cleaned or "quality" in cleaned:
            return "QA Engineer"
        if "security" in cleaned or "cyber" in cleaned or "infosec" in cleaned:
            return "Security Engineer"

        # General Software Engineer fallback
        return raw_role.strip() if len(raw_role.strip()) > 3 else "Software Engineer"

    @classmethod
    def resolve_candidate_role(
        cls,
        target_role: Optional[str] = None,
        jd_role: Optional[str] = None,
        resume_role: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Resolves candidate role priority:
        Explicit Target Role > JD Role > Resume Inferred Role
        Preserves all role sources for inspection.
        """
        resolved_raw = target_role or jd_role or resume_role or "Software Engineer"
        canonical = cls.normalize_role(resolved_raw)

        taxonomy_info = ROLE_TAXONOMY.get(canonical, {
            "canonical_role": canonical,
            "category": "General Engineering",
            "aliases": [canonical.lower()],
            "core_skills": ["Software Engineering", "Problem Solving", "System Architecture", "Git"],
            "category_distribution": {
                "Technical": 30,
                "Role-specific": 15,
                "Project/Experience": 15,
                "Problem solving": 10,
                "Situational": 10,
                "Behavioral": 10,
                "System design": 5,
                "Coding/Practical": 5
            }
        })

        return {
            "canonical_role": canonical,
            "resolved_role": resolved_raw,
            "target_role": target_role,
            "jd_role": jd_role,
            "resume_role": resume_role,
            "category": taxonomy_info["category"],
            "core_skills": taxonomy_info.get("core_skills", []),
            "category_distribution": taxonomy_info.get("category_distribution", {})
        }
