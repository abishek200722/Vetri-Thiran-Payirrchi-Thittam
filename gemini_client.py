from functools import lru_cache
from google import genai
from google.genai import types

from config import get_settings


class GeminiService:
    def __init__(self):
        settings = get_settings()
        if not settings.gemini_api_key:
            raise RuntimeError(
                "GEMINI_API_KEY is not configured. Add it to your environment or .env file."
            )
        self.client = genai.Client(api_key=settings.gemini_api_key)
        self.model = settings.gemini_model

    def generate(
        self,
        prompt: str,
        *,
        system_instruction: str | None = None,
        json_mode: bool = False,
        max_output_tokens: int = 1200,
    ) -> str:
        config_kwargs = {
            "temperature": 0.4,
            "max_output_tokens": max_output_tokens,
        }
        if system_instruction:
            config_kwargs["system_instruction"] = system_instruction
        if json_mode:
            config_kwargs["response_mime_type"] = "application/json"

        response = self.client.models.generate_content(
            model=self.model,
            contents=prompt,
            config=types.GenerateContentConfig(**config_kwargs),
        )
        text = getattr(response, "text", None)
        if not text:
            raise RuntimeError("Gemini returned an empty response.")
        return text.strip()


@lru_cache
def get_gemini_service() -> GeminiService:
    return GeminiService()
