from functools import lru_cache

from config import get_settings
from gemini_client import get_gemini_service
from prompts import EDUCATION_SYSTEM, EXPLAIN_PROMPT


@lru_cache
def _local_pipeline():
    from transformers import pipeline
    settings = get_settings()
    return pipeline(
        "text2text-generation",
        model=settings.local_explanation_model,
        device=-1,
    )


async def explain_concept(topic: str, level: str) -> str:
    settings = get_settings()

    if settings.enable_local_explanation:
        try:
            generator = _local_pipeline()
            prompt = (
                f"Explain {topic} simply for a {level} learner. "
                "Use short sentences and one example."
            )
            result = generator(prompt, max_new_tokens=220, do_sample=False)
            if result and result[0].get("generated_text"):
                return result[0]["generated_text"].strip()
        except Exception:
            # The local model is an optional lightweight path. If it cannot
            # load (for example, first-time download/network restrictions),
            # use the cloud model so the application remains usable.
            pass

    service = get_gemini_service()
    return service.generate(
        EXPLAIN_PROMPT.format(topic=topic, level=level),
        system_instruction=EDUCATION_SYSTEM,
        max_output_tokens=700,
    )
