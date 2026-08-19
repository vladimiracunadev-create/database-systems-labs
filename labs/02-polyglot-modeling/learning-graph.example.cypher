CREATE (ada:Student {id: 'STU-001', name: 'Estudiante Ada'}),
       (linus:Student {id: 'STU-002', name: 'Estudiante Linus'}),
       (db:Course {id: 'DB-101', title: 'Fundamentos de datos'}),
       (sql:Topic {id: 'SQL'}),
       (modeling:Topic {id: 'MODELING'}),
       (ada)-[:ENROLLED_IN {status: 'active'}]->(db),
       (linus)-[:ENROLLED_IN {status: 'active'}]->(db),
       (db)-[:TEACHES]->(sql),
       (db)-[:TEACHES]->(modeling),
       (ada)-[:MASTERED {evidence: 'SQL-01'}]->(sql);

MATCH (student:Student)-[:ENROLLED_IN]->(:Course)-[:TEACHES]->(topic:Topic)
WHERE NOT (student)-[:MASTERED]->(topic)
RETURN student.name AS student, collect(topic.id) AS pending_topics;
