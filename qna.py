from gemini_client import get_gemini_service
from prompts import EDUCATION_SYSTEM, QA_PROMPT


async def answer_question(question: str, level: str) -> str:
    service = get_gemini_service()
    return service.generate(
        QA_PROMPT.format(question=question, level=level),
        system_instruction=EDUCATION_SYSTEM,
        max_output_tokens=900,
    )
