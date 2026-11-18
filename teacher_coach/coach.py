from __future__ import annotations

import os

from .fallback import render_demo_answer
from .retrieval import Lesson, retrieve


SYSTEM_PROMPT = """You are Lesson Coach, a calm math teaching partner. Help teachers refresh mathematics and prepare lessons. Do not test, score, rank, judge, or certify the teacher. Use only the supplied lesson context for mathematical claims. If the context is insufficient, say so plainly. Be concise and practical. Always use these headings: The key idea; How to explain it; Likely misconceptions; Try this with students; A useful next step."""


def _context(lessons: list[Lesson]) -> str:
    chunks = []
    for lesson in lessons:
        chunks.append(f"Topic: {lesson.title}\nRefresher: {lesson.refresher}\nExplanation: {lesson.explanation}\nMisconceptions: {'; '.join(lesson.misconceptions)}\nPrompts: {'; '.join(lesson.prompts)}\nNext step: {lesson.next_step}")
    return "\n\n".join(chunks)


def answer(query: str, lessons: list[Lesson]) -> tuple[str, list[Lesson], str]:
    matches = retrieve(query, lessons)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        return render_demo_answer(query, matches), matches, "demo"
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        response = client.chat.completions.create(
            model=os.getenv("OPENAI_MODEL", "gpt-4o-mini"),
            temperature=0.2,
            max_tokens=600,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": f"Teacher request: {query}\n\nLesson context:\n{_context(matches) if matches else '[No matching lesson context]'}"},
            ],
        )
        return response.choices[0].message.content, matches, "model"
    except Exception as exc:
        return render_demo_answer(query, matches) + f"\n\n_Model unavailable; used demo mode ({type(exc).__name__})._", matches, "demo-fallback"
