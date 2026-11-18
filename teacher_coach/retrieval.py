from __future__ import annotations

import json
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Lesson:
    id: str
    title: str
    level: str
    keywords: list[str]
    refresher: str
    explanation: str
    misconceptions: list[str]
    prompts: list[str]
    next_step: str


def load_lessons() -> list[Lesson]:
    path = Path(__file__).parent / "content" / "lessons.json"
    return [Lesson(**item) for item in json.loads(path.read_text(encoding="utf-8"))]


def _tokens(text: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", text.lower()))


def retrieve(query: str, lessons: list[Lesson], limit: int = 2) -> list[Lesson]:
    query_tokens = _tokens(query)
    scored = []
    for lesson in lessons:
        searchable = _tokens(" ".join([lesson.title, lesson.level, *lesson.keywords, lesson.refresher]))
        score = len(query_tokens & searchable)
        if "equation" in query_tokens or "equations" in query_tokens or "unknown" in query_tokens or "x" in query_tokens:
            if lesson.id == "linear-equations":
                score += 3
        if "rectangle" in query_tokens or "rectangles" in query_tokens:
            if lesson.id == "area-rectangles":
                score += 3
        if "fraction" in query_tokens or "fractions" in query_tokens:
            if lesson.id == "equivalent-fractions":
                score += 3
        scored.append((score, lesson))
    scored.sort(key=lambda pair: pair[0], reverse=True)
    return [lesson for score, lesson in scored[:limit] if score > 0]
