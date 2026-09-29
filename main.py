from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from schemas import (
    ExplainRequest, QARequest, QuizRequest, SummarizeRequest,
    LearningPathRequest
)
from explanation_module import explain_concept
from qna import answer_question
from quiz_module import generate_quiz
from summary_module import summarize_text
from learning_path import get_learning_recommendations

BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="EduGenie - Google Gemini Powered Learning Assistant",
    version="1.0.0",
    description="A lightweight educational assistant with Gemini-powered Q&A, quizzes, summaries and learning paths."
)

app.mount("/static", StaticFiles(directory=BASE_DIR / "static"), name="static")
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))


@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get("/health")
async def health():
    return {"status": "ok", "service": "EduGenie"}


@app.post("/qa")
async def qa(payload: QARequest):
    return {"answer": await answer_question(payload.question, payload.level)}


@app.post("/explain")
async def explain(payload: ExplainRequest):
    return {"explanation": await explain_concept(payload.topic, payload.level)}


@app.post("/quiz")
async def quiz(payload: QuizRequest):
    return {"quiz": await generate_quiz(payload.text, payload.level)}


@app.post("/summarize")
async def summarize(payload: SummarizeRequest):
    return {"summary": await summarize_text(payload.text, payload.level)}


@app.post("/learn/recommendations")
async def recommendations(payload: LearningPathRequest):
    return {
        "recommendations": await get_learning_recommendations(
            payload.topic, payload.level, payload.hours_per_week
        )
    }
