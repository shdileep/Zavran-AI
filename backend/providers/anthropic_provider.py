import json
import urllib.request
import urllib.error
from typing import Dict, Any, List, Optional
from backend.config import settings
from backend.providers.llm_base import LLMProvider

class AnthropicProvider(LLMProvider):
    """
    Secondary LLM Provider using Anthropic API (Claude 3.5 Sonnet).
    Used as high-fidelity alternative and fallback provider.
    """

    def __init__(self, api_key: Optional[str] = None, model: Optional[str] = None):
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.model = model or settings.ANTHROPIC_MODEL
        self.base_url = "https://api.anthropic.com/v1/messages"

    def _call_messages_api(self, system_prompt: str, user_prompt: str) -> str:
        if not self.api_key:
            raise ValueError("ANTHROPIC_API_KEY is not configured in .env")

        headers = {
            "x-api-key": self.api_key,
            "anthropic-version": "2023-06-01",
            "Content-Type": "application/json",
            "User-Agent": "ZavranAI-Backend/1.0",
        }

        payload = {
            "model": self.model,
            "max_tokens": 4096,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
            "temperature": 0.2,
        }

        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(self.base_url, data=data, headers=headers, method="POST")

        try:
            with urllib.request.urlopen(req, timeout=45) as resp:
                result = json.loads(resp.read().decode("utf-8"))
                blocks = result.get("content", [])
                text_blocks = [b.get("text", "") for b in blocks if b.get("type") == "text"]
                return "".join(text_blocks)
        except urllib.error.HTTPError as e:
            err_body = e.read().decode("utf-8")
            raise RuntimeError(f"Anthropic API error ({e.code}): {err_body}")
        except Exception as e:
            raise RuntimeError(f"Anthropic connection error: {str(e)}")

    def _extract_json_block(self, text: str) -> Dict[str, Any]:
        text = text.strip()
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0].strip()
        elif "```" in text:
            text = text.split("```")[1].split("```")[0].strip()
        return json.loads(text)

    async def extract_resume(self, resume_text: str) -> Dict[str, Any]:
        system_prompt = (
            "You are a technical resume parser. Extract accurate candidate information from resume text into JSON. "
            "Output JSON with keys: name, summary, skills, experience, education, projects, certifications, technologies."
        )
        res_str = self._call_messages_api(system_prompt, f"Resume:\n{resume_text}")
        return self._extract_json_block(res_str)

    async def extract_job_description(self, jd_text: str) -> Dict[str, Any]:
        system_prompt = (
            "Analyze the Job Description. Output JSON with keys: job_title, required_skills, preferred_skills, "
            "responsibilities, technologies, experience_requirements, domain."
        )
        res_str = self._call_messages_api(system_prompt, f"JD:\n{jd_text}")
        return self._extract_json_block(res_str)

    async def generate_interview_plan(
        self, candidate_profile: Dict[str, Any], jd_profile: Dict[str, Any]
    ) -> List[Dict[str, Any]]:
        system_prompt = (
            "Generate a tailored interview question plan comparing resume to JD. "
            "Output JSON object with key 'questions' containing list of question objects with hidden_rubric."
        )
        prompt = f"Profile:\n{json.dumps(candidate_profile)}\n\nJD:\n{json.dumps(jd_profile)}"
        res_str = self._call_messages_api(system_prompt, prompt)
        parsed = self._extract_json_block(res_str)
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
            "Evaluate candidate answer against hidden rubric. Output JSON with keys: score (0-100), quality, "
            "correctness, technical_depth, communication, reasoning, resume_consistency, jd_relevance, action, "
            "interviewer_response, key_observations."
        )
        prompt = f"Question:\n{json.dumps(question)}\n\nAnswer:\n{answer_transcript}"
        res_str = self._call_messages_api(system_prompt, prompt)
        return self._extract_json_block(res_str)

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
            "Compile an exhaustive AI interview report. Output JSON with keys: overall_score, category_scores, "
            "strengths, improvement_areas, jd_alignment_items, resume_consistency_status, question_evaluations, recommendation, duration_seconds."
        )
        prompt = f"Summary Data:\nQuestions: {len(questions)}, Answers: {len(answers)}, Violations: {len(violations)}"
        res_str = self._call_messages_api(system_prompt, prompt)
        return self._extract_json_block(res_str)
