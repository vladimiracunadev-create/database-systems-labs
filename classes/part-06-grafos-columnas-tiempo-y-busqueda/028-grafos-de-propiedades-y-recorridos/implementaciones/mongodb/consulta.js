// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/reference/operator/aggregation/graphLookup/
// nota: $graphLookup hace el recorrido transitivo dentro del motor. Tiene un
//       limite de 100 MB por operacion y no aprovecha indices en colecciones
//       fragmentadas: sirve para jerarquias modestas, no para un grafo grande.

// === preparacion ===
db.prerrequisitos.drop();
db.prerrequisitos.insertMany([
  { curso: "AR-301", requiere: "SE-201" },
  { curso: "SE-201", requiere: "DB-101" },
  { curso: "DB-101", requiere: "MA-100" },
]);

// === consulta ===
db.prerrequisitos
  .aggregate([
    { $match: { curso: "AR-301" } },
    { $graphLookup: {
        from: "prerrequisitos",
        startWith: "$requiere",
        connectFromField: "requiere",
        connectToField: "curso",
        as: "cadena" } },
    { $project: { cursos: { $concatArrays: [["$requiere"], "$cadena.requiere"] } } },
    { $unwind: "$cursos" },
    { $group: { _id: "$cursos" } },
    { $sort: { _id: 1 } },
  ])
  .forEach((d) => print(d._id));
