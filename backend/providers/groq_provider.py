import json
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from backend.config import settings
from backend.providers.llm_base import LLMProvider

class GroqProvider(LLMProvider):
    """
    Fast Inference LLM Provider using Groq API.
    Provides ultra-low-latency evaluations and dynamic question transitions.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.GROQ_API_KEY
        self.model = model or settings.GROQ_MODEL
        self.base_url = "https://api.groq.com/openai/v1/chat/completions"

    def _call_groq(self, system_prompt: str, user_prompt: str) -> str:
        if not self.api_key:
            raise ValueError("GROQ_API_KEY is not configured in .env")

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "User-Agent": "ZavranAI-Backend/1.0",
        }

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.2,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.base_url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=30) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                return result["choices"][0]["message"]["content"]
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            raise RuntimeError(f"Groq API error ({e.code}): {err_body}")
        except Exception as e:
            raise RuntimeError(f"Groq connection error: {str(e)}")

    async def extract_resume(self, resume_text: str) -> Dict[str, Any]:
        system_prompt = (
            "Extract candidate profile from resume text into JSON format with keys: "
            "name, summary, skills, experience, education, projects, certifications, technologies."
        )
        res_str = self._call_groq(system_prompt, f"Resume:\n{resume_text}")
        return json.loads(res_str)

    async def extract_job_description(self, jd_text: str) -> Dict[str, Any]:
        system_prompt = (
            "Extract job requirements into JSON with keys: "
            "job_title, required_skills, preferred_skills, responsibilities, technologies, experience_requirements, domain."
        )
        res_str = self._call_groq(system_prompt, f"JD:\n{jd_text}")
        return json.loads(res_str)

    async def generate_interview_plan(
        self, candidate_profile: Dict[str, Any], jd_profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        system_prompt = (
            "Generate personalized technical interview questions. Output JSON with key 'questions' containing "
            "objects with id, step_label, category, question, hidden_rubric."
        )
        prompt = f"Profile:\n{json.dumps(candidate_profile)}\n\nJD:\n{json.dumps(jd_profile)}"
        res_str = self._call_groq(system_prompt, prompt)
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
            "Evaluate candidate answer. Return JSON with score (0-100), quality, correctness, technical_depth, "
            "communication, reasoning, resume_consistency, jd_relevance, action, interviewer_response, key_observations."
        )
        prompt = f"Question:\n{json.dumps(question)}\n\nCandidate Answer:\n{answer_transcript}"
        res_str = self._call_groq(system_prompt, prompt)
        return json.loads(res_str)

    async def generate_interviewer_response(
        self, evaluation: Dict[str, Any], next_question: Dict[str, Any]
    ) -> str:
        interviewer_response = evaluation.get("interviewer_response", "")
        next_q_text = next_question.get("question", "")
        return f"{interviewer_response} {next_q_text}".strip()

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
            "Compile comprehensive interview evaluation report. Return JSON with overall_score, category_scores, "
            "strengths, improvement_areas, jd_alignment_items, resume_consistency_status, question_evaluations, recommendation, duration_seconds."
        )
        prompt = f"Data:\nQuestions: {len(questions)}, Answers: {len(answers)}, Violations: {len(violations)}"
        res_str = self._call_groq(system_prompt, prompt)
        return json.loads(res_str)
