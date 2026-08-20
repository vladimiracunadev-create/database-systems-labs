// motor: neo4j
// doc: https://neo4j.com/docs/cypher-manual/current/constraints/
// nota: implementacion declarada. La restriccion de unicidad se declara sobre
//       una propiedad de nodo; MERGE busca antes de crear, asi que el tercer
//       estudiante no llega a duplicarse.

// === preparacion ===
MATCH (n:Estudiante) DETACH DELETE n;
CREATE CONSTRAINT correo_unico IF NOT EXISTS
  FOR (e:Estudiante) REQUIRE e.correo IS UNIQUE;
MERGE (:Estudiante {correo: 'ada@example.org'});
MERGE (:Estudiante {correo: 'linus@example.org'});
MERGE (:Estudiante {correo: 'ada@example.org'});

// === consulta ===
MATCH (e:Estudiante) RETURN e.correo AS correo ORDER BY correo;
