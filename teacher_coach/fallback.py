from .retrieval import Lesson


def render_demo_answer(query: str, lessons: list[Lesson]) -> str:
    if not lessons:
        return ("I do not have a lesson in my small demo library that matches this request. "
                "I would rather say that clearly than invent mathematics. Try fractions, "
                "one-step equations, or area of rectangles.")
    lesson = lessons[0]
    misconceptions = "\n".join(f"- {item}" for item in lesson.misconceptions)
    prompts = "\n".join(f"- {item}" for item in lesson.prompts)
    return f"""## The key idea\n{lesson.refresher}\n\n## How to explain it\n{lesson.explanation}\n\n## Likely misconceptions\n{misconceptions}\n\n## Try this with students\n{prompts}\n\n## A useful next step\n{lesson.next_step}\n\n_Demo mode: this answer is grounded in the local lesson library. Query: {query}_"""
