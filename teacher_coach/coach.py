from __future__ import annotations

import os

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:  # Keep the demo runnable before dependencies are installed.
    def load_dotenv() -> None:
        env_path = ".env"
        if not os.path.exists(env_path):
            return
        for line in open(env_path, encoding="utf-8"):
            line = line.strip()
            if line and not line.startswith("#") and "=" in line:
                key, value = line.split("=", 1)
                os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

from .fallback import render_demo_answer
from .retrieval import Lesson, retrieve


SYSTEM_PROMPT = """You are Lesson Coach, a calm math teaching partner. Help teachers refresh mathematics and prepare lessons. Do not test, score, rank, judge, or certify the teacher. Use only the supplied lesson context for mathematical claims. If the context is insufficient, say so plainly. Be concise and practical. Always use these headings: The key idea; How to explain it; Likely misconceptions; Try this with students; A useful next step."""


def _context(lessons: list[Lesson]) -> str:
    chunks = []
    for lesson in lessons:
        chunks.append(f"Topic: {lesson.title}\nRefresher: {lesson.refresher}\nExplanation: {lesson.explanation}\nMisconceptions: {'; '.join(lesson.misconceptions)}\nPrompts: {'; '.join(lesson.prompts)}\nNext step: {lesson.next_step}")
    return "\n\n".join(chunks)


def answer(query: str, lessons: list[Lesson]) -> tuple[str, list[Lesson], str]:
    load_dotenv()
    matches = retrieve(query, lessons, limit=1)
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434/v1")
    model = os.getenv("OLLAMA_MODEL", "llama3.2:3b")
    try:
        from openai import OpenAI
        client = OpenAI(api_key="ollama", base_url=base_url)
        response = client.chat.completions.create(
            model=model,
            temperature=0.2,
            max_tokens=int(os.getenv("OLLAMA_MAX_TOKENS", "1200")),
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Teacher request: {query}\n\nLesson context:\n{_context(matches) if matches else '[No matching lesson context]'}"},
            ],
        )
        return response.choices[0].message.content, matches, "model"
    except Exception as exc:
        return render_demo_answer(query, matches) + f"\n\n_Local Ollama unavailable; used demo mode ({type(exc).__name__})._", matches, "demo-fallback"

