from __future__ import annotations

from math import sqrt


DOCUMENTS = {
    "sql-basics": [0.95, 0.05, 0.10],
    "graph-paths": [0.10, 0.95, 0.15],
    "vector-rag": [0.15, 0.20, 0.98],
    "sql-indexes": [0.85, 0.10, 0.25],
}
QUERY = [0.90, 0.05, 0.20]
RELEVANT = {"sql-basics", "sql-indexes"}


def cosine(left: list[float], right: list[float]) -> float:
    dot = sum(a * b for a, b in zip(left, right, strict=True))
    left_norm = sqrt(sum(value * value for value in left))
    right_norm = sqrt(sum(value * value for value in right))
    return dot / (left_norm * right_norm)


def main() -> None:
    ranking = sorted(
        ((name, cosine(QUERY, vector)) for name, vector in DOCUMENTS.items()),
        key=lambda item: item[1],
        reverse=True,
    )
    top_k = [name for name, _ in ranking[:2]]
    recall_at_2 = len(set(top_k) & RELEVANT) / len(RELEVANT)

    assert top_k == ["sql-indexes", "sql-basics"]
    assert recall_at_2 == 1.0
    print("Ranking:", [(name, round(score, 4)) for name, score in ranking])
    print("recall@2:", recall_at_2)
    print("VECTOR_LAB_OK")


if __name__ == "__main__":
    main()
