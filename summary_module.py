from config import get_settings
from gemini_client import get_gemini_service
from prompts import EDUCATION_SYSTEM, SUMMARY_PROMPT


def _clip(text: str) -> str:
    return text[: get_settings().max_input_chars]


async def summarize_text(text: str, level: str) -> str:
    service = get_gemini_service()
    return service.generate(
        SUMMARY_PROMPT.format(text=_clip(text), level=level),
        system_instruction=EDUCATION_SYSTEM,
        max_output_tokens=900,
    )
