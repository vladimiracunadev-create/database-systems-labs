// motor: neo4j
// doc: https://neo4j.com/docs/cypher-manual/current/patterns/variable-length-patterns/
// nota: aqui esta la clase entera en dos caracteres. `*` significa «uno o mas
//       saltos», y el motor no resuelve cada salto por indice: cada nodo guarda
//       punteros a sus vecinos, asi que el costo depende del vecindario
//       recorrido y no del tamano del grafo.

// === preparacion ===
MATCH (n) DETACH DELETE n;
CREATE (ar:Curso {codigo: 'AR-301'}),
       (se:Curso {codigo: 'SE-201'}),
       (db:Curso {codigo: 'DB-101'}),
       (ma:Curso {codigo: 'MA-100'}),
       (ar)-[:REQUIERE]->(se),
       (se)-[:REQUIERE]->(db),
       (db)-[:REQUIERE]->(ma);

// === consulta ===
MATCH (:Curso {codigo: 'AR-301'})-[:REQUIERE*]->(previo:Curso)
RETURN DISTINCT previo.codigo AS curso
ORDER BY curso;
