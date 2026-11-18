from .coach import answer
from .retrieval import load_lessons


def main() -> None:
    lessons = load_lessons()
    print("Lesson Coach - grounded math lesson preparation")
    print("Try: Help me prepare a lesson on equivalent fractions")
    print("Type 'quit' to exit.\n")
    while True:
        query = input("Teacher request> ").strip()
        if query.lower() in {"quit", "exit"}:
            break
        if not query:
            continue
        response, matches, mode = answer(query, lessons)
        print(f"\n[{mode}; matched: {', '.join(x.title for x in matches) or 'none'}]\n")
        print(response)
        print("\n" + "-" * 72 + "\n")


if __name__ == "__main__":
    main()
