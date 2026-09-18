import json
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from backend.config import settings
from backend.providers.llm_base import LLMProvider

class GoogleAIProvider(LLMProvider):
    """
    Google AI Studio / Gemini LLM Provider.
    Implements full interview generation and evaluation contracts using Gemini models.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.GOOGLE_AI_STUDIO_API_KEY
        self.model = model or settings.GOOGLE_MODEL
        self.base_url = f"https://generativelanguage.googleapis.com/v1beta/models/{self.model}:generateContent"

    def _call_gemini(self, prompt: str) -> str:
        if not self.api_key:
            raise ValueError("GOOGLE_AI_STUDIO_API_KEY is not configured in .env")

        url = f"{self.base_url}?key={self.api_key}"
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "ZavranAI-Backend/1.0",
        }

        payload = {
            "contents": [{"parts": [{"text": prompt}]}],
            "generationConfig": {
                "temperature": 0.2,
                "responseMimeType": "application/json",
            },
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                candidates = result.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts:
                        return parts[0].get("text", "{}")
                return "{}"
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            raise RuntimeError(f"Google Gemini API error ({e.code}): {err_body}")
        except Exception as e:
            raise RuntimeError(f"Google Gemini connection error: {str(e)}")

    async def extract_resume(self, resume_text: str) -> Dict[str, Any]:
        prompt = (
            "Extract candidate profile from resume text into JSON format with keys: "
            "name, summary, skills, experience, education, projects, certifications, technologies.\n"
            f"Resume:\n{resume_text}"
        )
        res = self._call_gemini(prompt)
        return json.loads(res)

    async def extract_job_description(self, jd_text: str) -> Dict[str, Any]:
        prompt = (
            "Extract job requirements into JSON with keys: "
            "job_title, required_skills, preferred_skills, responsibilities, technologies, experience_requirements, domain.\n"
            f"JD:\n{jd_text}"
        )
        res = self._call_gemini(prompt)
        return json.loads(res)

    async def generate_interview_plan(
        self, candidate_profile: Dict[str, Any], jd_profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        prompt = (
            "Generate personalized interview question plan comparing resume to JD. "
            "Output JSON with key 'questions' containing question objects with hidden_rubric.\n"
            f"Profile:\n{json.dumps(candidate_profile)}\n\nJD:\n{json.dumps(jd_profile)}"
        )
        res = self._call_gemini(prompt)
        parsed = json.loads(res)
        return parsed.get("questions", [])

    async def evaluate_answer(
        self,
        question: Dict[str, Any],
        answer_transcript: str,
        candidate_profile: Dict[str, Any],
        jd_profile: Dict[str, Any],
        history: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        prompt = (
            "Evaluate candidate answer. Return JSON with score (0-100), quality, correctness, technical_depth, "
            "communication, reasoning, resume_consistency, jd_relevance, action, interviewer_response, key_observations.\n"
            f"Question:\n{json.dumps(question)}\n\nCandidate Answer:\n{answer_transcript}"
        )
        res = self._call_gemini(prompt)
        return json.loads(res)

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
        prompt = (
            "Compile comprehensive interview evaluation report. Return JSON with overall_score, category_scores, "
            "strengths, improvement_areas, jd_alignment_items, resume_consistency_status, question_evaluations, recommendation, duration_seconds.\n"
            f"Candidate: {json.dumps(candidate_profile)}\nJD: {json.dumps(jd_profile)}"
        )
        res = self._call_gemini(prompt)
        return json.loads(res)
