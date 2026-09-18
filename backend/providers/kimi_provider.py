import json
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from backend.config import settings
from backend.providers.llm_base import LLMProvider

class KimiProvider(LLMProvider):
    """
    Kimi / Moonshot AI Intelligence Provider.
    Implements OpenAI-compatible API interface for deep reasoning question generation,
    candidate response evaluation, JD understanding, and adaptive follow-up creation.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        base_url: Optional[str] = None,
        model: Optional[str] = None,
    ):
        self.api_key = api_key or settings.KIMI_API_KEY
        self.base_url = (base_url or settings.KIMI_BASE_URL or "https://api.moonshot.cn/v1").rstrip("/") + "/chat/completions"
        self.model = model or settings.KIMI_MODEL or "moonshot-v1-32k"

    def _call_chat_completion(self, system_prompt: str, user_prompt: str, response_json: bool = True) -> str:
        """Helper to invoke Kimi / Moonshot API with robust JSON parsing and error handling."""
        if not self.api_key:
            raise ValueError("KIMI_API_KEY is not configured in .env")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "ZavranAI-Backend/2.0",
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
            with urllib.request.urlopen(req, timeout=50) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            raise RuntimeError(f"Kimi API error ({e.code}): {err_body}")
        except Exception as e:
            raise RuntimeError(f"Kimi connection error: {str(e)}")

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
            "You are an enterprise talent architect for Zavran AI. Analyze the provided Job Description (JD) and "
            "extract required technical competencies, domain, and experience levels into strict JSON.\n"
            "Return JSON matching:\n"
            "{\n"
            '  "job_title": "",\n'
            '  "role": "",\n'
            '  "seniority": "",\n'
            '  "required_skills": [],\n'
            '  "preferred_skills": [],\n'
            '  "skills": [],\n'
            '  "tools": [],\n'
            '  "responsibilities": [],\n'
            '  "technologies": [],\n'
            '  "experience_requirements": "",\n'
            '  "required_experience": "",\n'
            '  "nice_to_have_skills": [],\n'
            '  "domain": ""\n'
            "}"
        )
        user_prompt = f"Job Description:\n{jd_text}"
        res_str = self._call_chat_completion(system_prompt, user_prompt, response_json=True)
        return json.loads(res_str)

    async def generate_interview_plan(
        self, candidate_profile: Dict[str, Any], jd_profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        target_role = jd_profile.get("job_title") or jd_profile.get("role") or "Full Stack AI Engineer"
        system_prompt = (
            "You are the Lead AI Technical Interview Architect for Zavran AI. "
            "Generate a highly personalized, structured question set tailored specifically to the role and Job Description. "
            "Return a JSON object containing a 'questions' array. Each question must have:\n"
            "- question_id: 'Q01', 'Q02', etc.\n"
            "- category: Technical, Coding, System Design, Architecture, Problem Solving, Role-specific knowledge, Scenario-based, Behavioral, etc.\n"
            "- topic: string\n"
            "- skill: primary skill tested\n"
            "- difficulty: 'easy', 'medium', 'hard', or 'expert'\n"
            "- question: detailed interview question text\n"
            "- ideal_answer: comprehensive benchmark answer (for private evaluation only)\n"
            "- evaluation_criteria: list of strings\n"
            "- expected_concepts: list of critical concepts required in a strong response\n"
            "- red_flags: list of critical misconceptions or disqualifying claims\n"
            "- follow_up_questions: list of 2 adaptive follow-up questions\n"
            "- estimated_time_seconds: int (e.g. 90 or 120)\n"
            "CRITICAL: Never mention Zarun. The platform is Zavran AI."
        )
        user_prompt = (
            f"Role: {target_role}\n"
            f"Candidate Profile: {json.dumps(candidate_profile)}\n"
            f"Job Description Profile: {json.dumps(jd_profile)}"
        )
        res_str = self._call_chat_completion(system_prompt, user_prompt, response_json=True)
        parsed = json.loads(res_str)
        if isinstance(parsed, dict) and "questions" in parsed:
            return parsed["questions"]
        elif isinstance(parsed, list):
            return parsed
        return []

    async def evaluate_answer(
        self,
        question: Dict[str, Any],
        answer_transcript: str,
        candidate_profile: Dict[str, Any],
        jd_profile: Dict[str, Any],
        history: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        system_prompt = (
            "You are an expert Senior Staff Interviewer evaluating a candidate's response for Zavran AI. "
            "Evaluate the answer with extreme rigor against the expected concepts and ideal answer.\n"
            "Return JSON matching:\n"
            "{\n"
            '  "score": 0-100,\n'
            '  "quality": "weak|average|good|excellent",\n'
            '  "depth_level": 1-5,\n'
            '  "demonstrated_concepts": [],\n'
            '  "missing_concepts": [],\n'
            '  "incorrect_claims": [],\n'
            '  "strengths_observed": [],\n'
            '  "areas_for_improvement": [],\n'
            '  "followup_needed": true/false,\n'
            '  "recommended_followup_direction": "",\n'
            '  "feedback": ""\n'
            "}"
        )
        user_prompt = (
            f"Question:\n{json.dumps(question)}\n\n"
            f"Candidate Answer Transcript:\n{answer_transcript}"
        )
        res_str = self._call_chat_completion(system_prompt, user_prompt, response_json=True)
        return json.loads(res_str)

    async def generate_adaptive_followup(
        self,
        current_question: Dict[str, Any],
        candidate_answer: str,
        evaluation: Dict[str, Any],
        next_difficulty: str = "medium"
    ) -> Dict[str, Any]:
        system_prompt = (
            "You are an adaptive AI technical interviewer for Zavran AI. "
            "Based on the candidate's actual answer and the evaluation (concepts covered vs missed), "
            "generate a precise, natural follow-up question that either probes missing depth or explores an edge case.\n"
            "Return JSON matching:\n"
            "{\n"
            '  "question": "",\n'
            '  "category": "Follow-up",\n'
            '  "skill": "",\n'
            '  "difficulty": "easy|medium|hard|expert",\n'
            '  "ideal_answer": "",\n'
            '  "expected_concepts": [],\n'
            '  "evaluation_criteria": [],\n'
            '  "red_flags": []\n'
            "}"
        )
        user_prompt = (
            f"Current Question: {current_question.get('question')}\n"
            f"Candidate Answer: {candidate_answer}\n"
            f"Demonstrated Concepts: {evaluation.get('demonstrated_concepts', [])}\n"
            f"Missing Concepts: {evaluation.get('missing_concepts', [])}\n"
            f"Evaluation Quality: {evaluation.get('quality', 'average')}\n"
            f"Target Difficulty: {next_difficulty}"
        )
        res_str = self._call_chat_completion(system_prompt, user_prompt, response_json=True)
        return json.loads(res_str)

    async def generate_interviewer_response(
        self, evaluation: Dict[str, Any], next_question: Dict[str, Any]
    ) -> str:
        score = evaluation.get("score", 70)
        q_text = next_question.get("question", "")
        if score >= 85:
            prefix = "Excellent explanation. That demonstrates strong architectural depth."
        elif score >= 65:
            prefix = "Thank you. That covers the practical fundamentals nicely."
        else:
            prefix = "Understood, thank you for sharing that approach."
        return f"{prefix} Let's move to the next area: {q_text}"
