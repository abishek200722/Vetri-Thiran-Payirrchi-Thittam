from pydantic import BaseModel, Field, field_validator


class TextRequest(BaseModel):
    level: str = Field(default="beginner", max_length=30)

    @field_validator("level")
    @classmethod
    def normalize_level(cls, value: str) -> str:
        value = value.strip().lower()
        allowed = {"school", "beginner", "intermediate", "advanced"}
        return value if value in allowed else "beginner"


class QARequest(TextRequest):
    question: str = Field(min_length=2, max_length=20000)


class ExplainRequest(TextRequest):
    topic: str = Field(min_length=2, max_length=500)


class QuizRequest(TextRequest):
    text: str = Field(min_length=20, max_length=20000)


class SummarizeRequest(TextRequest):
    text: str = Field(min_length=20, max_length=20000)


class LearningPathRequest(TextRequest):
    topic: str = Field(min_length=2, max_length=300)
    hours_per_week: float = Field(default=5, ge=1, le=40)
