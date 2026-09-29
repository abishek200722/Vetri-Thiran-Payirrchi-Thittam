import os
from dataclasses import dataclass
from functools import lru_cache


@dataclass(frozen=True)
class Settings:
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-3.8-flash")
    local_explanation_model: str = os.getenv(
        "LOCAL_EXPLANATION_MODEL",
        "MBZUAI/LaMini-Flan-T5-783M"
    )
    enable_local_explanation: bool = os.getenv(
        "ENABLE_LOCAL_EXPLANATION", "true"
    ).lower() in {"1", "true", "yes", "on"}
    max_input_chars: int = int(os.getenv("MAX_INPUT_CHARS", "20000"))


@lru_cache
def get_settings() -> Settings:
    return Settings()
