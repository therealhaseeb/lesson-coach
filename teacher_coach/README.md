# Lesson Coach

Lesson Coach is a small, grounded prototype for math teachers who want to refresh their own understanding and prepare a lesson without being tested, scored, or judged.

## Run it

Requires Python 3.10+.

```powershell
python -m teacher_coach.app
```

Ask a question such as:

> Help me prepare a lesson on equivalent fractions for grade 5.

The app uses a local open-weight model through Ollama. It does not use a hosted LLM API or require an API key.

```powershell
pip install -r requirements.txt
Copy-Item .env.example .env
ollama run qwen3:1.7b
python -m teacher_coach.app
```

The app also supports local open-weight models served through an OpenAI-compatible endpoint. For example, with Ollama:

```powershell
ollama run qwen3:1.7b
# Edit .env if you want to change the model or Ollama URL.
python -m teacher_coach.app
```

If Ollama is not running, the app automatically returns the existing hard-coded fallback response. The local model receives only the teacher request and selected lesson context.

The default response budget is 1,200 tokens. Increase `OLLAMA_MAX_TOKENS` in `.env` if a local model still truncates an answer.

## Retrieval workflow

This prototype does not use a vector database and does not perform embedding-based semantic search. It loads the small local `content/lessons.json` library, tokenizes the teacher request, scores lessons by overlapping words, and applies explicit bridges for phrases such as `x + 3 = 8`, `fractions`, and `rectangle`. The top matches are placed in the local model prompt. A production version could replace this function with embeddings and a vector database later.

Run the checks:

```powershell
python -m teacher_coach.evaluate
```

## Product decision

The prototype focuses on lesson preparation, not general chat. A teacher enters a topic or goal and receives a short mathematics refresher, a teachable explanation, likely misconceptions, classroom prompts, and a next step. There are no tests, scores, certificates, or teacher judgments.

## Architecture

1. `content/lessons.json` contains a small, inspectable lesson library.
2. `retrieval.py` uses lightweight token matching to select relevant lesson material.
3. `coach.py` builds a grounded prompt and calls the model when configured.
4. Without an API key, `fallback.py` provides a transparent demo response from the same lesson material.
5. `evaluate.py` runs a small regression set for relevance, grounding, usefulness, and safe handling of unsupported topics.

The retrieval interface is intentionally replaceable: a production version could swap token matching for embeddings and a managed vector store without changing the coach contract.

## Quality approach

The evaluation set includes supported questions, a misconception-focused question, and an unsupported topic. Each result is checked for a relevant lesson, required answer sections, and an explicit limitation when the library does not cover the request. This is a prototype evaluation, not a claim of educational validation.

## Cost and scaling

Illustrative assumption: 20 lesson-preparation requests per active teacher per month, 1,200 input tokens and 700 output tokens per request, using a low-cost model. The calculation is:

```text
20 × (1,200 input tokens + 700 output tokens) × model price / 1,000,000
```

The exact number depends on the chosen provider and current pricing. Costs can be reduced by keeping lesson context short, caching common topics, using a small model for routing, and pre-generating explanations for frequently requested lessons.

## Data and compliance

The prototype sends the teacher's typed request and selected lesson context to the configured model provider. It does not ask for or store student names, student records, or other personal data. The demo keeps no conversation history. In production, add retention limits, deletion controls, access controls, provider data-processing review, and clear guidance not to enter identifiable student information.

## Scope and trade-offs

Skipped deliberately: accounts, polished frontend, full curriculum coverage, multilingual support, vector infrastructure, analytics, and persistent personalization. These would be appropriate after validating that teachers find the grounded lesson-preparation flow useful.

## Two-hour implementation log

The intended assignment workflow is represented by the commit history: establish the prototype, add retrieval, add generation/fallback, then add evaluation and documentation. The implementation prioritizes a working, explainable vertical slice over feature count.

