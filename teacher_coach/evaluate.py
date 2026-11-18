from .coach import answer
from .retrieval import load_lessons


CASES = [
    ("Help me prepare equivalent fractions for grade 5", "Equivalent fractions", True),
    ("What misconceptions should I expect when teaching x + 3 = 8?", "One-step linear equations", True),
    ("Give me a lesson idea for rectangle area", "Area of rectangles", True),
    ("Help me teach calculus limits", None, False),
]


def main() -> None:
    lessons = load_lessons()
    passed = 0
    for query, expected, supported in CASES:
        text, matches, _ = answer(query, lessons)
        has_expected = expected is None or any(item.title == expected for item in matches)
        has_sections = (not supported) or all(section in text for section in ["The key idea", "How to explain it", "Likely misconceptions"])
        handles_gap = supported or "do not have" in text.lower() or "insufficient" in text.lower()
        ok = has_expected and has_sections and handles_gap
        print(f"{'PASS' if ok else 'FAIL'}: {query}")
        if not ok:
            print(f"  matches={matches!r}; sections={has_sections}; gap={handles_gap}")
        passed += ok
    print(f"\n{passed}/{len(CASES)} evaluation cases passed")
    raise SystemExit(0 if passed == len(CASES) else 1)


if __name__ == "__main__":
    main()
