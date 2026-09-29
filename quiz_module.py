import json
import re

from config import get_settings
from gemini_client import get_gemini_service
from prompts import EDUCATION_SYSTEM, QUIZ_PROMPT


def clean_json_block(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text, flags=re.IGNORECASE)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def _validate_quiz(data: dict) -> dict:
    questions = data.get("questions")
    if not isinstance(questions, list) or len(questions) != 3:
        raise ValueError("Gemini did not return exactly 3 questions.")

    for item in questions:
        if not isinstance(item, dict):
            raise ValueError("Invalid quiz question.")
        options = item.get("options")
        answer = item.get("answer")
        if not isinstance(options, list) or len(options) != 4:
            raise ValueError("Each question must contain exactly 4 options.")
        if answer not in options:
            raise ValueError("The answer must match one of the options.")
    return data


async def generate_quiz(text: str, level: str) -> dict:
    settings = get_settings()
    service = get_gemini_service()
    prompt = QUIZ_PROMPT.format(text=text[:settings.max_input_chars], level=level)

    raw = service.generate(
        prompt,
        system_instruction=EDUCATION_SYSTEM,
        json_mode=True,
        max_output_tokens=1300,
    )
    return _validate_quiz(json.loads(clean_json_block(raw)))
