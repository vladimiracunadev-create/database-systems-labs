// motor: neo4j
// doc: https://neo4j.com/docs/cypher-manual/current/clauses/optional-match/
// nota: implementacion declarada. OPTIONAL MATCH es la reunion externa: si el
//       patron no encuentra pareja, las variables del patron quedan en null y
//       la fila del estudiante sobrevive.

// === preparacion ===
MATCH (n) DETACH DELETE n;
CREATE (a:Estudiante {nombre: 'Ada'}),
       (l:Estudiante {nombre: 'Linus'}),
       (g:Estudiante {nombre: 'Grace'}),
       (db:Curso {codigo: 'DB-101'}),
       (se:Curso {codigo: 'SE-201'}),
       (a)-[:INSCRITO_EN]->(db),
       (a)-[:INSCRITO_EN]->(se),
       (l)-[:INSCRITO_EN]->(db);

// === consulta ===
MATCH (e:Estudiante)
OPTIONAL MATCH (e)-[:INSCRITO_EN]->(c:Curso)
RETURN e.nombre AS nombre, coalesce(c.codigo, 'sin-curso') AS codigo
ORDER BY nombre, codigo;
