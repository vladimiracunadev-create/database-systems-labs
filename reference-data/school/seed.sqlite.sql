INSERT INTO students (student_id, display_name, created_at) VALUES
    (1, 'Estudiante Ada', '2026-03-01T09:00:00Z'),
    (2, 'Estudiante Linus', '2026-03-01T09:00:00Z'),
    (3, 'Estudiante Grace', '2026-03-01T09:00:00Z'),
    (4, 'Estudiante Margaret', '2026-03-01T09:00:00Z');

INSERT INTO courses (course_id, code, title) VALUES
    (10, 'DB-101', 'Fundamentos de datos'),
    (20, 'SE-201', 'Ingeniería de software');

INSERT INTO enrollments (student_id, course_id, status, enrolled_at) VALUES
    (1, 10, 'active', '2026-03-02'),
    (2, 10, 'active', '2026-03-02'),
    (3, 10, 'active', '2026-03-02'),
    (4, 10, 'withdrawn', '2026-03-02'),
    (1, 20, 'active', '2026-03-02'),
    (3, 20, 'active', '2026-03-02');

INSERT INTO assessments (assessment_id, course_id, title, max_score, due_at) VALUES
    (100, 10, 'Modelo conceptual', 100, '2026-03-15'),
    (110, 10, 'Consultas SQL', 100, '2026-03-30'),
    (200, 20, 'ADR inicial', 100, '2026-04-05');

INSERT INTO submissions (submission_id, assessment_id, student_id, score, submitted_at) VALUES
    (1000, 100, 1, 92, '2026-03-14'),
    (1001, 100, 2, 58, '2026-03-15'),
    (1002, 100, 3, 81, '2026-03-13'),
    (1010, 110, 1, 88, '2026-03-29'),
    (1011, 110, 3, 76, '2026-03-28'),
    (2000, 200, 1, 90, '2026-04-04');
