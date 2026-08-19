PRAGMA foreign_keys = ON;

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    display_name TEXT NOT NULL,
    created_at TEXT NOT NULL
);

CREATE TABLE courses (
    course_id INTEGER PRIMARY KEY,
    code TEXT NOT NULL UNIQUE,
    title TEXT NOT NULL
);

CREATE TABLE enrollments (
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    status TEXT NOT NULL CHECK (status IN ('active', 'completed', 'withdrawn')),
    enrolled_at TEXT NOT NULL,
    PRIMARY KEY (student_id, course_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id),
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE assessments (
    assessment_id INTEGER PRIMARY KEY,
    course_id INTEGER NOT NULL,
    title TEXT NOT NULL,
    max_score REAL NOT NULL CHECK (max_score > 0),
    due_at TEXT NOT NULL,
    FOREIGN KEY (course_id) REFERENCES courses(course_id)
);

CREATE TABLE submissions (
    submission_id INTEGER PRIMARY KEY,
    assessment_id INTEGER NOT NULL,
    student_id INTEGER NOT NULL,
    score REAL NOT NULL CHECK (score >= 0),
    submitted_at TEXT NOT NULL,
    UNIQUE (assessment_id, student_id),
    FOREIGN KEY (assessment_id) REFERENCES assessments(assessment_id),
    FOREIGN KEY (student_id) REFERENCES students(student_id)
);

CREATE INDEX idx_assessments_course ON assessments(course_id);
CREATE INDEX idx_submissions_student ON submissions(student_id);
