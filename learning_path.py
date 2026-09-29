from gemini_client import get_gemini_service
from prompts import EDUCATION_SYSTEM, LEARNING_PATH_PROMPT


async def get_learning_recommendations(
    topic: str, level: str, hours_per_week: float
) -> str:
    service = get_gemini_service()
    return service.generate(
        LEARNING_PATH_PROMPT.format(
            topic=topic,
            level=level,
            hours_per_week=hours_per_week,
        ),
        system_instruction=EDUCATION_SYSTEM,
        max_output_tokens=1500,
    )
