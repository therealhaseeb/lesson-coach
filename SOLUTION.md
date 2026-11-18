# Lesson Coach - Solution Document

## 1. Executive summary

Lesson Coach is a grounded AI assistant for math teachers who want to refresh their own subject knowledge and prepare lessons independently.

The prototype deliberately avoids presenting itself as a generic chatbot, test, examiner, or scoring system. A teacher asks for help with a topic and receives a structured preparation aid:

1. the key mathematical idea;
2. a way to explain it;
3. likely student misconceptions;
4. classroom prompts;
5. a practical next step for the teacher.

The solution is intentionally small. The assignment rewards understanding, product judgment, answer quality, cost awareness, and communication more than feature count. The prototype therefore demonstrates one complete, explainable vertical slice.

## 2. Problem understanding

The user is a math teacher who may lack confidence in the mathematics behind a lesson. This teacher:

- learns alone and online;
- uses a web browser or simple digital tool;
- dislikes chatbot-style interaction;
- does not want tests, judgment, scores, exams, or certificates;
- has a reliable internet connection.

The product must feel like a calm preparation tool, not an assessment system. It should help the teacher feel more ready to teach without making the teacher feel evaluated.

The scale assumption is important: 20,000-50,000 teachers may use the product. A design that sends long conversations and large documents to a premium model for every request would be unnecessarily expensive.

## 3. Product decision

### Chosen product: lesson preparation coach

The first prototype focuses on a single need: preparing to teach a known math topic.

The teacher asks something like:

> Help me prepare a lesson on equivalent fractions for grade 5.

The coach answers with a predictable structure rather than an open-ended conversation.

### Why this scope

This scope is useful, narrow enough to implement quickly, and aligned with the brief. It also creates a clear quality target: can a teacher use the response to prepare a lesson?

### Deliberately excluded

The prototype does not include:

- tests or quizzes;
- scores, rankings, or certificates;
- teacher performance judgments;
- student accounts or student data;
- full curriculum coverage;
- persistent personalization;
- a polished frontend;
- authentication;
- analytics dashboards.

These features may be useful later, but they would distract from proving the core coaching experience.

## 4. User experience

The current prototype uses a command-line interface because the assignment says a frontend is optional. The interface is sufficient to demonstrate the product behavior and keeps almost all effort focused on retrieval, prompting, answer quality, evaluation, and explanation.

Example:

```text
Teacher request> Help me prepare a lesson on equivalent fractions
```

The response is organized into:

- `The key idea`
- `How to explain it`
- `Likely misconceptions`
- `Try this with students`
- `A useful next step`

This structure makes answers scannable and gives the teacher practical classroom value.

## 5. Architecture

```text
Teacher request
      |
      v
Lightweight topic retrieval
      |
      v
Relevant lesson context
      |
      +----------------------+
      |                      |
      v                      v
LLM generation        Deterministic fallback
      |                      |
      +----------+-----------+
                 v
       Structured teacher answer
```

### Components

#### `app.py`

Owns the interactive loop. It reads teacher requests, calls the coach, displays the selected mode and matched lessons, and prints the answer.

#### `content/lessons.json`

Contains the small lesson library. Each lesson has:

- an identifier and title;
- level information;
- keywords;
- a mathematical refresher;
- an explanation strategy;
- likely misconceptions;
- classroom prompts;
- a next step.

The data is intentionally inspectable. A reviewer can read the source material and understand what the coach knows.

#### `retrieval.py`

Loads the lesson library and performs lightweight token matching. It also contains a few plain-language bridges for common teacher phrasing, such as mapping `x + 3 = 8` or `unknown` to one-step equations.

The retrieval function has a small, replaceable interface. A production implementation could use embeddings, a vector database, or a curriculum taxonomy without requiring changes to the user-facing coach contract.

#### `coach.py`

Coordinates retrieval and generation. It sends the teacher request and selected lesson context only to a local Ollama open-weight model. If Ollama is unavailable, it returns the deterministic fallback.

The model prompt requires the coach to:

- act as a calm math teaching partner;
- avoid testing, scoring, ranking, judgment, and certification;
- use only the supplied lesson context for mathematical claims;
- state when the context is insufficient;
- use the required answer sections;
- remain concise and practical.

#### `fallback.py`

Provides a useful response without a model. It renders the lesson content directly into the same answer structure. This makes the prototype easy to run, cheap to demo, and resilient to API failure.

#### `evaluate.py`

Runs a small regression set covering supported topics, symbolic input, and an unsupported topic. It checks retrieval, answer structure, and graceful handling of gaps.

## 6. Technology choices

### Python

Python was chosen because:

- it is widely understood by engineering teams;
- it is fast to prototype in;
- JSON, text processing, and model SDK integration are simple;
- it allows a clean CLI without frontend overhead.

### JSON lesson store

JSON is appropriate for the first version because the lesson library is small, versionable, readable, and easy to edit. A database would add infrastructure without improving the two-hour prototype.

### Token retrieval

Token matching is intentionally simple. It has transparent behavior, no infrastructure cost, and no embedding-model dependency. It is not sufficient for a large curriculum, but it is a good prototype boundary.

### Local open-weight model integration

The only model path is a local open-weight model served by Ollama through its local OpenAI-compatible endpoint. There is no hosted LLM API path and no API key is required. The model is used for language generation, not as the source of truth for the curriculum.

### CLI instead of frontend

The brief says a frontend is optional. A CLI maximizes the time spent on the important engineering questions: grounding, answer shape, evaluation, cost, and data flow.

## 7. Why the model is grounded

An unconstrained language model could produce mathematically incorrect or pedagogically unsuitable advice. This prototype reduces that risk by:

1. keeping a curated lesson library;
2. retrieving relevant material before generation;
3. placing the retrieved material in the model context;
4. instructing the model to use only that context for mathematical claims;
5. returning a limitation when no matching lesson exists;
6. evaluating representative questions.

This is not a complete correctness guarantee. It is a practical prototype control that is easy to explain and extend.

## 8. Demo mode versus model mode

### Demo mode

When no API key is configured:

```text
Question -> local retrieval -> stored lesson response
```

Advantages:

- no cost;
- no network call;
- deterministic behavior;
- easy reviewer setup;
- useful offline fallback.

Trade-off: responses are less flexible and mostly limited to the curated material.

### Model mode

When Ollama is running locally:

```text
Question -> local retrieval -> grounded prompt -> model -> structured answer
```

Advantages:

- more natural wording;
- better adaptation to teacher phrasing;
- ability to combine the retrieved lesson material into a tailored explanation.

Trade-off: local model calls introduce hardware requirements, latency, model-quality variation, and residual hallucination risk.

### Local open-weight mode

The application uses Ollama's local OpenAI-compatible endpoint. For example:

```powershell
ollama run llama3.2:3b
$env:OLLAMA_BASE_URL = "http://localhost:11434/v1"
$env:OLLAMA_MODEL = "llama3.2:3b"
python -m teacher_coach.app
```

This keeps the request and lesson context on the local machine, removes per-request API cost, and makes experimentation with open-weight models easy. The trade-offs are local RAM/CPU/GPU requirements, potentially slower or weaker responses, and the need to install and operate Ollama.

## Retrieval and semantic-search decision

The prototype does not use a vector database. It uses lexical retrieval: tokenizing the request, counting overlaps with lesson titles, keywords, and refreshers, then applying explicit phrase bridges. This is not embedding-based semantic search. It is transparent and adequate for three lessons, but it will miss synonyms and longer conceptual relationships. A production upgrade would add embeddings and a vector store while keeping the same retrieval interface.

### Failure behavior

If the model call fails, the app falls back to the deterministic response. This preserves a working user experience and makes failures visible rather than silently returning an empty answer.

## 9. Evaluation strategy

The prototype includes four regression cases:

1. equivalent fractions;
2. one-step linear equations expressed with `x + 3 = 8`;
3. rectangle area;
4. unsupported calculus limits.

For supported questions, the checks confirm:

- the expected lesson is retrieved;
- the required answer sections appear.

For unsupported questions, the check confirms that the coach states that the lesson library does not cover the topic rather than inventing an answer.

### What this evaluation does not prove

The regression suite does not prove:

- mathematical correctness for all possible prompts;
- teacher satisfaction;
- learning outcomes;
- curriculum alignment across countries;
- safety in every language;
- production reliability.

The next evaluation stage would use a larger expert-reviewed test set and teacher feedback.

## 10. Cost model

The assignment asks for cost per teacher per month. The prototype uses a simple planning model rather than pretending to know a final production bill.

Illustrative assumptions:

- 20 lesson-preparation requests per active teacher per month;
- 1,200 input tokens per request;
- 700 output tokens per request;
- a low-cost model tier.

The formula is:

```text
monthly cost per teacher
= requests per month
  × (input tokens + output tokens)
  × model price per token
```

The exact price must be filled in using the selected provider's current pricing at production planning time.

### Cost controls

- retrieve only the relevant lesson context;
- keep system and user prompts short;
- cache repeated topic requests;
- use a small model for routing or classification;
- use a stronger model only when needed;
- pre-generate common lesson material;
- avoid sending unnecessary conversation history;
- retain no chat history by default.

At 20,000-50,000 teachers, these controls matter more than optimizing a few lines of Python.

## 11. Data flow and compliance

### Demo mode

The teacher's request is processed locally against the local JSON lesson library. No model provider is contacted.

### Model mode

The application sends:

- the teacher's typed request;
- the selected lesson context;
- the system instructions needed to produce the answer.

The application does not ask for student names, student records, or identifiable student information.

### Production requirements

Before production, clarify:

- provider data-processing terms;
- data retention and deletion;
- regional hosting requirements;
- access controls and audit logs;
- encryption in transit and at rest;
- model-provider training and retention settings;
- a clear rule against entering identifiable student data;
- incident response and abuse reporting.

The prototype's privacy posture is intentionally simple: no persistent conversation history and no student data model.

## 12. Extensibility

The design leaves clear upgrade points:

### Retrieval

Replace token matching with embeddings, curriculum metadata, or a hybrid search system.

### Content

Expand from three lessons to a versioned curriculum with source citations, grade levels, languages, and regional adaptations.

### Model routing

Use a small classifier to decide whether a request is lesson preparation, subject refresh, or unsupported.

### User interface

Add a browser interface with topic suggestions, answer sections, copy/export controls, and a clear source-context panel.

### Quality

Add expert review, golden answers, factuality checks, citation coverage, latency tracking, and teacher feedback.

### Operations

Add authentication, rate limits, monitoring, cost budgets, feature flags, and provider failover.

## 13. What was skipped and why

The assignment gives two hours and explicitly values understanding and quality over completeness. The following were skipped intentionally:

| Skipped item | Reason |
|---|---|
| Full web frontend | Frontend is optional; CLI demonstrates the core loop faster |
| Vector database | Three lessons do not justify infrastructure |
| Authentication | Not needed to demonstrate the product decision |
| Persistent history | Conflicts with the simplest privacy posture |
| Full curriculum | Would reduce time for evaluation and explanation |
| Multilingual support | Important later, but not testable in this prototype |
| Student workflows | The chosen user is the teacher preparing a lesson |
| Analytics | No validated usage questions yet |

## 14. Suggested interview presentation

### Opening

“I chose to build a grounded lesson-preparation coach rather than a general chatbot because the teacher needs confidence and practical preparation, while explicitly rejecting tests and judgment.”

### Demo

Show:

1. a normal equivalent-fractions request;
2. a symbolic equation request;
3. an unsupported calculus request;
4. the evaluation command.

### Architecture discussion

Explain that the lesson library is the source of truth, retrieval controls context, the model is optional, and fallback mode keeps the prototype runnable.

### Trade-off discussion

Defend the CLI, JSON content store, token retrieval, small lesson set, and explicit skipped work as deliberate time-boxed choices.

### Quality discussion

Explain that the current evaluation is a regression safety net, not a claim of educational validation. The next step is expert review and teacher testing.

### Cost and compliance discussion

Describe the per-teacher calculation, caching and context controls, and the fact that no student data is requested or persisted.

## 15. Limitations and risks

The most important risks are:

- incomplete curriculum coverage;
- retrieval misses caused by simple matching;
- model hallucination when context is insufficient;
- overly generic advice;
- culturally or regionally inappropriate pedagogy;
- teacher over-reliance on generated explanations;
- incorrect cost assumptions if usage differs from the plan.

The prototype makes these risks visible. It does not claim to solve them completely.

## 16. Final assessment

This solution is intentionally modest but defensible. It demonstrates:

- product judgment about a specific teacher need;
- a working end-to-end coaching loop;
- grounded model use;
- graceful no-model behavior;
- a replaceable architecture;
- a concrete evaluation strategy;
- cost awareness;
- a simple data and compliance story;
- clear scope management.

That is the right level of ambition for a two-hour technical assignment where explanation and trade-offs matter more than feature volume.

