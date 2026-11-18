# Lesson Coach

A grounded AI math lesson-preparation coach for teachers.

Lesson Coach helps a teacher refresh the mathematics behind a topic and prepare a lesson without tests, scores, judgment, or certificates. The prototype deliberately focuses on a small, explainable vertical slice rather than a generic chatbot.

## Quick start

Requires Python 3.10+.

```powershell
python -m teacher_coach.app
```

Try:

```
Help me prepare a lesson on equivalent fractions for grade 5
```

The app runs in deterministic demo mode without credentials. For model-backed generation, install the optional dependency and configure an OpenAI-compatible API key:

```powershell
pip install -e ".[model]"
$env:OPENAI_API_KEY = "..."
python -m teacher_coach.app
```

Run the regression checks:

```powershell
python -m teacher_coach.evaluate
```

## Product decision

The prototype is a lesson-preparation coach, not open-ended chat. A teacher enters a topic or lesson goal and receives:

- a mathematics refresher;
- a teachable explanation;
- likely misconceptions;
- classroom prompts;
- a practical next step.

The response is grounded in a small local lesson library. When the topic is not covered, the demo says so instead of inventing content.

## Architecture

```text
Teacher request
      |
      v
Lightweight topic retrieval
      |
      v
Grounded lesson context
      |
      v
LLM response or deterministic fallback
      |
      v
Structured teacher-facing answer
```

- `teacher_coach/content/lessons.json` contains inspectable lesson material.
- `retrieval.py` selects relevant material with lightweight token matching.
- `coach.py` builds the grounded prompt and optionally calls a model.
- `fallback.py` keeps the app runnable and predictable without an API key.
- `evaluate.py` checks supported topics, required sections, and unsupported-topic behavior.

The retrieval boundary is replaceable: production could use embeddings and a managed vector store without changing the coach interface.

## Evaluation

The included checks cover:

1. equivalent fractions;
2. a symbolic one-step equation query;
3. rectangle area;
4. an unsupported calculus query.

Each supported response is checked for a matching lesson and required answer sections. The unsupported query is checked for a clear limitation. This is a prototype regression suite, not a claim of formal educational validation.

## Cost and scaling

Illustrative planning assumption: 20 lesson-preparation requests per active teacher per month, with 1,200 input tokens and 700 output tokens per request.

```text
monthly cost per teacher
= 20 × (1,200 input tokens + 700 output tokens) × model price / 1,000,000
```

The exact result depends on the selected provider and current pricing. Costs can be reduced by:

- keeping retrieved context short;
- caching common topics;
- using a small model for routing;
- reserving a stronger model for difficult explanations;
- pre-generating high-frequency lesson material;
- avoiding unnecessary conversation history.

## Data and compliance

The prototype sends the teacher's typed request and selected lesson context to the configured model provider. It does not request or store student names, student records, or other personal data, and the demo keeps no conversation history.

For production, add retention limits, deletion controls, access controls, provider data-processing review, regional hosting decisions, and clear guidance not to enter identifiable student information.

## Scope and trade-offs

Skipped deliberately:

- accounts and authentication;
- a polished frontend;
- full curriculum coverage;
- multilingual support;
- vector database infrastructure;
- analytics;
- persistent personalization.

These are reasonable next steps after validating that teachers find the grounded lesson-preparation flow useful. The prototype prioritizes a working, explainable vertical slice over feature count.

## Repository structure

```text
teacher_coach/
  app.py                 # interactive CLI
  coach.py               # grounded generation
  evaluate.py            # regression checks
  fallback.py            # deterministic demo responses
  retrieval.py           # lesson loading and retrieval
  content/lessons.json   # curated lesson library
pyproject.toml
```

## Assignment delivery notes

The project was designed for a two-hour technical assignment: choose a narrow teacher need, build a working prototype, explain trade-offs, evaluate answer quality, estimate cost, and document data handling.