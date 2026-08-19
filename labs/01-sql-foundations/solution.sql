-- 1. Matrículas por curso y estado.
SELECT c.code, e.status, COUNT(*) AS enrollment_count
FROM courses c
JOIN enrollments e ON e.course_id = c.course_id
GROUP BY c.course_id, c.code, e.status
ORDER BY c.code, e.status;

-- 2. Promedios, conservando evaluaciones sin entregas.
SELECT a.title, ROUND(AVG(s.score), 1) AS average_score
FROM assessments a
LEFT JOIN submissions s ON s.assessment_id = a.assessment_id
GROUP BY a.assessment_id, a.title
ORDER BY average_score DESC;

-- 3. Progreso por estudiante y curso.
SELECT st.display_name, c.code,
       ROUND(100.0 * COUNT(sub.submission_id) / COUNT(a.assessment_id), 1) AS completion_pct
FROM enrollments e
JOIN students st ON st.student_id = e.student_id
JOIN courses c ON c.course_id = e.course_id
JOIN assessments a ON a.course_id = e.course_id
LEFT JOIN submissions sub
  ON sub.student_id = e.student_id
 AND sub.assessment_id = a.assessment_id
WHERE e.status = 'active'
GROUP BY st.student_id, st.display_name, c.course_id, c.code;

-- 4. Riesgo por bajo promedio o ausencia de entregas.
SELECT st.display_name, AVG(sub.score) AS average_score
FROM students st
JOIN enrollments e ON e.student_id = st.student_id AND e.status = 'active'
LEFT JOIN submissions sub ON sub.student_id = st.student_id
GROUP BY st.student_id, st.display_name
HAVING AVG(sub.score) < 60 OR AVG(sub.score) IS NULL;

-- 5. Ranking por curso.
WITH course_average AS (
  SELECT e.course_id, e.student_id, AVG(sub.score) AS average_score
  FROM enrollments e
  JOIN assessments a ON a.course_id = e.course_id
  LEFT JOIN submissions sub
    ON sub.assessment_id = a.assessment_id
   AND sub.student_id = e.student_id
  WHERE e.status = 'active'
  GROUP BY e.course_id, e.student_id
)
SELECT course_id, student_id, average_score,
       DENSE_RANK() OVER (PARTITION BY course_id ORDER BY average_score DESC) AS course_rank
FROM course_average;

-- 8. En una API, suministra el valor mediante el mecanismo de parámetros
-- del driver. El signo ? es el marcador de SQLite y no se reemplaza por texto.
SELECT course_id, code, title FROM courses WHERE code = ?;
