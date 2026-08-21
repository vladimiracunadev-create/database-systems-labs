// motor: neo4j
// doc: https://neo4j.com/docs/cypher-manual/current/patterns/
// nota: no hay tabla intermedia. La relacion de muchos a muchos es la arista
//       misma, y el diagrama entidad-relacion se parece tanto al modelo fisico
//       que el paso de uno a otro deja de ser una traduccion.

// === preparacion ===
MATCH (n) DETACH DELETE n;
CREATE (a:Estudiante {nombre: 'Ada'}),
       (l:Estudiante {nombre: 'Linus'}),
       (:Estudiante {nombre: 'Grace'}),
       (db:Curso {codigo: 'DB-101'}),
       (se:Curso {codigo: 'SE-201'}),
       (:Curso {codigo: 'AR-301'}),
       (a)-[:INSCRITO_EN]->(db),
       (a)-[:INSCRITO_EN]->(se),
       (l)-[:INSCRITO_EN]->(db);

// === consulta ===
MATCH (c:Curso)
OPTIONAL MATCH (e:Estudiante)-[:INSCRITO_EN]->(c)
RETURN c.codigo AS curso, count(e) AS estudiantes
ORDER BY curso;
