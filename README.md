# Lesson Coach

A grounded AI math lesson-preparation coach for teachers.

## Quick start on Windows

Requires Python 3.10+, Git, and [Ollama](https://ollama.com).

```powershell
git clone https://github.com/therealhaseeb/lesson-coach.git
cd lesson-coach
pip install -r requirements.txt
Copy-Item .env.example .env
ollama pull qwen3:1.7b
```

Start Ollama in one PowerShell window:

```powershell
ollama run qwen3:1.7b
```

Start Lesson Coach in a second PowerShell window:

```powershell
python -m teacher_coach.app
```

Try:

```text
Help me prepare a lesson on equivalent fractions
```

Run the checks:

```powershell
python -m teacher_coach.evaluate
```

## Configuration

The app reads `.env` automatically:

```env
OLLAMA_BASE_URL=http://localhost:11434/v1
OLLAMA_MODEL=qwen3:1.7b
OLLAMA_MAX_TOKENS=1200
```

No hosted LLM API or API key is required. If Ollama is unavailable, the app uses the deterministic hard-coded fallback response.

## Workflow

```text
Teacher question
      ↓
Local lesson retrieval
      ↓
Relevant lesson context
      ↓
Local Qwen model through Ollama
      ↓
Structured teaching response
```

The response contains the key idea, an explanation strategy, likely misconceptions, classroom prompts, and a next step.

## Retrieval

The prototype does not use a vector database or embedding-based semantic search. It loads `teacher_coach/content/lessons.json`, tokenizes the teacher request, scores overlapping words, and applies a few explicit bridges for phrases such as `x + 3 = 8`, `fractions`, and `rectangle`. A production version could replace this with embeddings and a vector database.

## Repository structure

```text
teacher_coach/
  app.py
  coach.py
  evaluate.py
  fallback.py
  retrieval.py
  content/lessons.json
requirements.txt
.env.example
SOLUTION.md
```

See [SOLUTION.md](SOLUTION.md) for the full architecture, decisions, technology choices, evaluation, cost, privacy, limitations, and interview presentation plan.

