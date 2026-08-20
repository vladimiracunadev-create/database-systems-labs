// motor: neo4j
// doc: https://neo4j.com/docs/cypher-manual/current/clauses/where/
// nota: el mismo algebra con otra forma: el patron es la reunion, el WHERE la
//       seleccion y el RETURN la proyeccion.

// === preparacion ===
MATCH (n) DETACH DELETE n;
CREATE (a:Estudiante {nombre: 'Ada'}),
       (l:Estudiante {nombre: 'Linus'}),
       (g:Estudiante {nombre: 'Grace'}),
       (db:Curso {codigo: 'DB-101'}),
       (se:Curso {codigo: 'SE-201'}),
       (a)-[:CURSO {nota: 90}]->(db),
       (l)-[:CURSO {nota: 58}]->(db),
       (g)-[:CURSO {nota: 72}]->(db),
       (a)-[:CURSO {nota: 66}]->(se),
       (g)-[:CURSO {nota: 78}]->(se);

// === consulta ===
MATCH (e:Estudiante)-[r:CURSO]->(c:Curso)
WHERE c.codigo = 'DB-101' AND r.nota >= 60
RETURN e.nombre AS nombre, r.nota AS nota
ORDER BY nombre;
