import json
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from backend.config import settings
from backend.providers.llm_base import LLMProvider

class OpenAIProvider(LLMProvider):
    """
    Primary LLM Intelligence Provider using OpenAI API.
    Responsible for Resume/JD understanding, question planning, hidden rubrics,
    answer evaluation, adaptive follow-ups, and final report compilation.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.OPENAI_API_KEY
        self.model = model or settings.OPENAI_MODEL
        self.base_url = "https://api.openai.com/v1/chat/completions"

    def _call_chat_completion(self, system_prompt: str, user_prompt: str, response_json: bool = True) -> str:
        """Helper to invoke OpenAI chat completion with robust error handling."""
        if not self.api_key:
            raise ValueError("OPENAI_API_KEY is not configured in .env")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "ZavranAI-Backend/1.0",
        }

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "temperature": 0.2,
        }
        if response_json:
            payload["response_format"] = {"type": "json_object"}

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.base_url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            raise RuntimeError(f"OpenAI API error ({e.code}): {err_body}")
        except Exception as e:
            raise RuntimeError(f"OpenAI connection error: {str(e)}")

    async def extract_resume(self, resume_text: str) -> Dict[str, Any]:
        system_prompt = (
            "You are an expert technical resume parser for Zavran AI. "
            "Extract accurate candidate information from the resume text into strict JSON. "
            "CRITICAL: Do NOT invent, hallucinate, or assume any details not present in the text. "
            "Return JSON matching:\n"
            "{\n"
            '  "name": "",\n'
            '  "summary": "",\n'
            '  "skills": [],\n'
            '  "experience": [{"company": "", "role": "", "period": "", "highlights": []}],\n'
            '  "education": [{"degree": "", "institution": "", "year": ""}],\n'
            '  "projects": [{"title": "", "description": "", "technologies": []}],\n'
            '  "certifications": [],\n'
            '  "technologies": []\n'
            "}"
        )
        user_prompt = f"Resume Text:\n{resume_text}"
        res_str = self._call_chat_completion(system_prompt, user_prompt, response_json=True)
        return json.loads(res_str)

    async def extract_job_description(self, jd_text: str) -> Dict[str, Any]:
        system_prompt = (
            "You are an enterprise talent architect. Analyze the provided Job Description (JD) and "
            "extract required technical competencies, domain, and experience levels into strict JSON.\n"
            "Return JSON matching:\n"
            "{\n"
            '  "job_title": "",\n'
            '  "required_skills": [],\n'
            '  "preferred_skills": [],\n'
            '  "responsibilities": [],\n'
            '  "technologies": [],\n'
            '  "experience_requirements": [],\n'
            '  "domain": ""\n'
            "}"
        )
        user_prompt = f"Job Description:\n{jd_text}"
        res_str = self._call_chat_completion(system_prompt, user_prompt, response_json=True)
        return json.loads(res_str)

    async def generate_interview_plan(
        self, candidate_profile: Dict[str, Any], jd_profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        system_prompt = (
            "You are the Lead AI Technical Interview Architect for Zavran AI. "
            "Generate an authoritatively structured, rigorous question bank of exactly 20 prepared interview questions "
            "based on deep analysis of the candidate's actual resume and the target Job Description (JD).\n\n"
            "QUESTION POOL STRUCTURE:\n"
            "- QUESTIONS 1-3 (Resume-based Depth): Deep technical probes investigating the candidate's actual claimed projects, tools, frameworks, and architecture choices (e.g. why that architecture, scale, failure modes, trade-offs).\n"
            "- QUESTIONS 4-10 (~7 questions, Mixed Resume + JD): Practical technical scenarios connecting candidate's claimed experience to the target role's expectations.\n"
            "- QUESTIONS 11-20 (~10 questions, Pure JD Role-Fit): Practical engineering scenarios, architecture reasoning, debugging under pressure, production edge cases, scaling, latency trade-offs, and failure handling.\n\n"
            "RULES:\n"
            "- Every question must contain all required internal metadata.\n"
            "- NEVER ask shallow definitions (e.g. 'What is X?'). Prefer practical scenarios: 'Your API latency spikes 10x during peak traffic. Walk me through your diagnosis.'\n"
            "- NEVER reveal internal evaluation rubrics or hints in the question text.\n"
            "Return JSON matching:\n"
            "{\n"
            '  "questions": [\n'
            '    {\n'
            '      "question_id": "Q01",\n'
            '      "question": "...",\n'
            '      "category": "...",\n'
            '      "topic": "...",\n'
            '      "source": "resume",\n'
            '      "concepts_tested": ["concept1", "concept2"],\n'
            '      "expected_answer_dimensions": ["dimension1", "dimension2"],\n'
            '      "expected_depth": "Level 3 - Applied",\n'
            '      "followup_strategy": ["followup probe 1", "followup probe 2"],\n'
            '      "difficulty": "Medium",\n'
            '      "evaluation_points": ["point1", "point2"]\n'
            '    }\n'
            '  ]\n'
            "}"
        )
        user_prompt = (
            f"Candidate Profile:\n{json.dumps(candidate_profile, indent=2)}\n\n"
            f"Target Job Description:\n{json.dumps(jd_profile, indent=2)}"
        )
        res_str = self._call_chat_completion(system_prompt, user_prompt, response_json=True)
        parsed = json.loads(res_str)
        return parsed.get("questions", [])

    async def evaluate_answer(
        self,
        question: Dict[str, Any],
        answer_transcript: str,
        candidate_profile: Dict[str, Any],
        jd_profile: Dict[str, Any],
        history: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        system_prompt = (
            "You are a Senior Principal Interview Evaluator for Zavran AI. "
            "Evaluate the candidate's spoken response against the hidden rubric, their actual resume, and the target JD.\n"
            "Evaluate:\n"
            "- Correctness (0-100)\n"
            "- Technical Depth (0-100)\n"
            "- Communication & Clarity (0-100)\n"
            "- Reasoning & Problem Solving (0-100)\n"
            "- Resume Consistency (true/false, flag discrepancies if they claim things contrary to their resume)\n"
            "- Overall Answer Quality ('strong', 'average', 'weak', 'incorrect')\n"
            "- Next Action Decision: One of ['DEEPER_FOLLOW_UP', 'CLARIFICATION', 'SIMPLIFY', 'CHALLENGE', 'NEW_TOPIC', 'MOVE_FORWARD']\n"
            "- Interlocutor Feedback Dialogue: A professional 1-2 sentence spoken response acknowledging their point without revealing scores or saying repetitive 'Great answer!'\n\n"
            "Return JSON matching:\n"
            "{\n"
            '  "score": 85,\n'
            '  "quality": "strong",\n'
            '  "correctness": 88,\n'
            '  "technical_depth": 85,\n'
            '  "communication": 82,\n'
            '  "reasoning": 84,\n'
            '  "resume_consistency": true,\n'
            '  "jd_relevance": 90,\n'
            '  "action": "DEEPER_FOLLOW_UP",\n'
            '  "interviewer_response": "That is a solid architecture approach. Let us look closer at how you handled...",\n'
            '  "key_observations": ["Demonstrated deep understanding of caching", "Clearly articulated latency trade-offs"]\n'
            "}"
        )
        user_prompt = (
            f"Question:\n{json.dumps(question, indent=2)}\n\n"
            f"Candidate Spoken Answer Transcript:\n\"{answer_transcript}\"\n\n"
            f"Candidate Profile Summary:\n{json.dumps(candidate_profile.get('skills', []), indent=2)}\n\n"
            f"Interview History Context:\n{json.dumps(history[-2:] if history else [], indent=2)}"
        )
        res_str = self._call_chat_completion(system_prompt, user_prompt, response_json=True)
        return json.loads(res_str)

    async def generate_interviewer_response(
        self, evaluation: Dict[str, Any], next_question: Dict[str, Any]
    ) -> str:
        interviewer_response = evaluation.get("interviewer_response", "")
        next_q_text = next_question.get("question", "")
        if interviewer_response:
            return f"{interviewer_response} {next_q_text}"
        return next_q_text

    async def generate_final_report(
        self,
        candidate_profile: Dict[str, Any],
        jd_profile: Dict[str, Any],
        questions: List[Dict[str, Any]],
        answers: List[Dict[str, Any]],
        evaluations: List[Dict[str, Any]],
        violations: List[Dict[str, Any]],
        duration_seconds: int,
        completion_reason: str,
    ) -> Dict[str, Any]:
        system_prompt = (
            "You are the Chief Evaluation Officer for Zavran AI. "
            "Compile an exhaustive, objective, and executive-ready final AI interview assessment report.\n"
            "CRITICAL RULES:\n"
            "- Base the report strictly on the candidate's actual answers, resume alignment, and JD requirements.\n"
            "- If the interview was terminated due to integrity/camera violations, the final recommendation MUST be 'Unsuccessful'.\n"
            "- Provide structured category scores, strengths, improvement areas, JD alignment checklist, and question breakdown.\n"
            "Return JSON matching:\n"
            "{\n"
            '  "overall_score": 84,\n'
            '  "category_scores": {\n'
            '    "technical_knowledge": 86,\n'
            '    "project_understanding": 88,\n'
            '    "problem_solving": 80,\n'
            '    "communication": 85,\n'
            '    "jd_alignment": 84,\n'
            '    "resume_consistency": 95\n'
            '  },\n'
            '  "strengths": ["...", "..."],\n'
            '  "improvement_areas": ["...", "..."],\n'
            '  "jd_alignment_items": [\n'
            '    {"skill": "Python", "status": "Demonstrated", "notes": "Strong mastery"},\n'
            '    {"skill": "FastAPI", "status": "Demonstrated", "notes": "Solid async implementation"}\n'
            '  ],\n'
            '  "resume_consistency_status": "Consistent",\n'
            '  "question_evaluations": [\n'
            '    {\n'
            '      "question": "...",\n'
            '      "answer": "...",\n'
            '      "score": 85,\n'
            '      "what_went_well": "...",\n'
            '      "what_could_improve": "..."\n'
            '    }\n'
            '  ],\n'
            '  "recommendation": "Strong Fit", # One of: ["Strong Fit", "Potential Fit", "Needs Improvement", "Not Recommended", "Unsuccessful"]\n'
            '  "completion_reason": "completed",\n'
            '  "duration_seconds": 1800\n'
            "}"
        )
        user_prompt = (
            f"Candidate:\n{json.dumps(candidate_profile, indent=2)}\n\n"
            f"Job Description:\n{json.dumps(jd_profile, indent=2)}\n\n"
            f"Questions:\n{json.dumps(questions, indent=2)}\n\n"
            f"Answers:\n{json.dumps(answers, indent=2)}\n\n"
            f"Evaluations:\n{json.dumps(evaluations, indent=2)}\n\n"
            f"Violations:\n{json.dumps(violations, indent=2)}\n\n"
            f"Session Duration: {duration_seconds}s, Completion Reason: {completion_reason}"
        )
        res_str = self._call_chat_completion(system_prompt, user_prompt, response_json=True)
        return json.loads(res_str)
