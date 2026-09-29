# EduGenie — Google Gemini Powered Learning Assistant

EduGenie is a lightweight educational assistant based on the supplied project documentation. The documented workflow calls for FastAPI, a simple HTML/CSS frontend, Gemini for Q&A/summarization/quiz/learning paths, and LaMini-Flan-T5 for concept explanations.

The project is implemented here as a complete runnable application with:

- FastAPI backend
- HTML/CSS/vanilla JavaScript frontend
- Gemini integration through the current `google-genai` SDK
- Optional local LaMini-Flan-T5 explanation path
- Q&A
- Concept explanation
- 3-question MCQ generation with four options each
- Text summarization
- Personalized learning path
- Health endpoint
- Request validation
- Automated API smoke tests
- `.env` secret configuration
- Docker support

## Project structure

```text
EduGenie/
├── main.py
├── config.py
├── gemini_client.py
├── schemas.py
├── prompts.py
├── explanation_module.py
├── qna.py
├── quiz_module.py
├── summary_module.py
├── learning_path.py
├── requirements.txt
├── .env.example
├── .gitignore
├── Dockerfile
├── README.md
├── templates/
│   └── index.html
├── static/
│   ├── style.css
│   └── app.js
└── tests/
    └── test_app.py
```

## Important API-key note

The source document contains an example-looking Gemini key. Do **not** copy that key into the project. Treat any key appearing in documentation as compromised and create/use your own key.

The frontend never receives the Gemini key. The browser talks to FastAPI, and FastAPI talks to Gemini.

## 1. Requirements

- Python 3.10+
- VS Code
- Internet access for Gemini API
- A Gemini API key

The local LaMini model downloads from Hugging Face the first time it is used. If you want the fastest setup or do not want that download, set:

```env
ENABLE_LOCAL_EXPLANATION=false
```

Concept explanation will then use Gemini too.

## 2. Open in VS Code

Open the `EduGenie` folder in VS Code.

Open the integrated terminal:

```text
Terminal → New Terminal
```

## 3. Create a virtual environment

### Windows

```powershell
py -3.10 -m venv .venv
.venv\Scripts\activate
```

### macOS/Linux

```bash
python3 -m venv .venv
source .venv/bin/activate
```

Verify:

```bash
python --version
```

## 4. Install dependencies

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

If PyTorch installation is problematic on your machine, first install the appropriate PyTorch build for your CPU/GPU from the official PyTorch instructions, then run the requirements command again.

## 5. Configure Gemini

Copy:

```text
.env.example
```

to:

```text
.env
```

Then put your own key in `.env`:

```env
GEMINI_API_KEY=YOUR_REAL_KEY
```

You can also choose the model:

```env
GEMINI_MODEL=gemini-3.8-flash
```

Never commit `.env` to Git.

## 6. Run the application

```bash
uvicorn main:app --reload
```

Open:

```text
http://127.0.0.1:8000
```

FastAPI API documentation is available at:

```text
http://127.0.0.1:8000/docs
```

Health check:

```text
http://127.0.0.1:8000/health
```

## 7. Test the application

Run the automated smoke tests:

```bash
pytest -q
```

For manual testing, try:

### Q&A

Task: `Q&A`

Input:

```text
What is the largest ocean?
```

### Explanation

Task: `Explain a concept`

Input:

```text
Explain the Pythagoras theorem
```

### Quiz

Task: `Generate quiz`

Paste a paragraph with at least a few sentences. The application asks Gemini for exactly 3 MCQs with 4 options each.

### Summary

Task: `Summarize`

Paste an educational passage.

### Learning path

Task: `Recommend learning path`

Input:

```text
SQL
```

Choose the learner level and available hours per week.

## API examples

### Q&A

```bash
curl -X POST http://127.0.0.1:8000/qa ^
  -H "Content-Type: application/json" ^
  -d "{\"question\":\"What is photosynthesis?\",\"level\":\"beginner\"}"
```

macOS/Linux:

```bash
curl -X POST http://127.0.0.1:8000/qa \
  -H "Content-Type: application/json" \
  -d '{"question":"What is photosynthesis?","level":"beginner"}'
```

### Explain

```bash
curl -X POST http://127.0.0.1:8000/explain \
  -H "Content-Type: application/json" \
  -d '{"topic":"recursion in Python","level":"beginner"}'
```

### Quiz

```bash
curl -X POST http://127.0.0.1:8000/quiz \
  -H "Content-Type: application/json" \
  -d '{"text":"Photosynthesis is the process by which green plants use sunlight to make food from carbon dioxide and water.","level":"school"}'
```

## Architecture

```text
Browser
  │
  │ POST JSON
  ▼
FastAPI
  ├── /qa ──────────────────────► Gemini
  ├── /explain ──► LaMini-T5 ───► fallback Gemini
  ├── /quiz ─────────────────────► Gemini JSON mode
  ├── /summarize ────────────────► Gemini
  └── /learn/recommendations ────► Gemini
```

## Design decisions

### Gemini SDK

The original project material uses the older `google.generativeai` package in several snippets. This implementation uses the current Google Gen AI SDK (`google-genai`) instead. The application calls `client.models.generate_content(...)`, keeps the API key server-side, and uses Gemini JSON mode for quiz output.

### Local explanation

The project documentation specifies `MBZUAI/LaMini-Flan-T5-783M` for concept explanation. The implementation keeps that model as the default local path but makes it lazy-loaded. If it cannot be loaded, the endpoint falls back to Gemini rather than crashing the server.

### Quiz reliability

The quiz endpoint asks for JSON and validates:
- exactly 3 questions
- exactly 4 options
- answer must be one of the options

### Secret management

The API key is read from an environment variable. Do not put it in HTML, JavaScript, Git, or a public repository.

## Docker

Build:

```bash
docker build -t edugenie .
```

Run:

```bash
docker run --rm -p 8000:8000 --env-file .env edugenie
```

Then open:

```text
http://127.0.0.1:8000
```

For a small production deployment, use a managed secret store instead of copying `.env` onto the server.

## Troubleshooting

### `GEMINI_API_KEY is not configured`

Make sure `.env` exists in the project root and contains:

```env
GEMINI_API_KEY=...
```

Restart the terminal/server after changing environment settings.

### Gemini model error

Change `GEMINI_MODEL` to a Gemini model available to your API account.

### First explanation is slow

LaMini-Flan-T5 may be downloading its model files. This happens only on first use and can require substantial disk/RAM.

For a simpler setup:

```env
ENABLE_LOCAL_EXPLANATION=false
```

### Port already in use

Run:

```bash
uvicorn main:app --reload --port 8001
```

## Security checklist

- Keep API keys secret.
- Do not commit `.env`.
- Keep Gemini calls on the backend.
- Restrict API keys where supported.
- Add authentication/rate limiting before exposing this publicly.
- Add logging/monitoring and a production secret manager for deployment.

## Future enhancements

The source project suggests voice interaction, multilingual support, mobile support, progress tracking, gamification, adaptive learning, group study, teacher/parent dashboards, LMS integration, image/PDF input, and notifications as future directions.
