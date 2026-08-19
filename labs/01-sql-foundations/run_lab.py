from __future__ import annotations

import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "reference-data" / "school"


def rows(connection: sqlite3.Connection, statement: str) -> list[tuple]:
    return connection.execute(statement).fetchall()


def main() -> None:
    connection = sqlite3.connect(":memory:")
    connection.executescript((DATA / "schema.sqlite.sql").read_text(encoding="utf-8"))
    connection.executescript((DATA / "seed.sqlite.sql").read_text(encoding="utf-8"))

    active_students = rows(
        connection,
        """
        SELECT c.code, COUNT(*) AS active_students
        FROM courses c
        JOIN enrollments e ON e.course_id = c.course_id
        WHERE e.status = 'active'
        GROUP BY c.course_id, c.code
        ORDER BY c.code
        """,
    )
    assert active_students == [("DB-101", 3), ("SE-201", 2)]

    averages = rows(
        connection,
        """
        SELECT s.display_name, ROUND(AVG(sub.score), 1) AS average_score
        FROM students s
        JOIN enrollments e ON e.student_id = s.student_id AND e.status = 'active'
        JOIN assessments a ON a.course_id = e.course_id
        LEFT JOIN submissions sub
          ON sub.assessment_id = a.assessment_id
         AND sub.student_id = s.student_id
        WHERE e.course_id = 10
        GROUP BY s.student_id, s.display_name
        ORDER BY s.student_id
        """,
    )
    assert averages == [
        ("Estudiante Ada", 90.0),
        ("Estudiante Linus", 58.0),
        ("Estudiante Grace", 78.5),
    ]

    pending = rows(
        connection,
        """
        SELECT s.display_name, a.title
        FROM enrollments e
        JOIN students s ON s.student_id = e.student_id
        JOIN assessments a ON a.course_id = e.course_id
        LEFT JOIN submissions sub
          ON sub.student_id = e.student_id
         AND sub.assessment_id = a.assessment_id
        WHERE e.status = 'active' AND sub.submission_id IS NULL
        ORDER BY s.student_id, a.assessment_id
        """,
    )
    assert pending == [
        ("Estudiante Linus", "Consultas SQL"),
        ("Estudiante Grace", "ADR inicial"),
    ]

    print("Active students:", active_students)
    print("DB-101 averages:", averages)
    print("Pending submissions:", pending)
    print("LAB_OK")


if __name__ == "__main__":
    main()
