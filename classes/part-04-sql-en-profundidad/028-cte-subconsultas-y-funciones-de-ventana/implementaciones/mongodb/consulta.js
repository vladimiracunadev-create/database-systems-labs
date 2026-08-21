// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/reference/operator/aggregation/setWindowFields/
// nota: $setWindowFields es la ventana: partitionBy es el PARTITION BY y
//       sortBy es el ORDER BY de dentro de la ventana. Y aqui aparece un
//       limite que SQL no tiene: $documentNumber, $rank y $denseRank exigen un
//       sortBy de UNA sola clave, asi que no se puede desempatar por un
//       segundo criterio como hace el ROW_NUMBER de la version SQL.

// === preparacion ===
db.notas.drop();
db.notas.insertMany([
  { estudiante: "Ada", curso: "DB-101", nota: 90 },
  { estudiante: "Linus", curso: "DB-101", nota: 58 },
  { estudiante: "Grace", curso: "DB-101", nota: 72 },
  { estudiante: "Ada", curso: "SE-201", nota: 66 },
  { estudiante: "Grace", curso: "SE-201", nota: 78 },
]);

// === consulta ===
db.notas
  .aggregate([
    { $setWindowFields: {
        partitionBy: "$curso",
        sortBy: { nota: -1 },
        output: { puesto: { $documentNumber: {} } } } },
    { $match: { puesto: 1 } },
    { $project: { _id: 0, curso: 1, estudiante: 1, nota: 1 } },
    { $sort: { curso: 1 } },
  ])
  .forEach((d) => print(d.curso + "|" + d.estudiante + "|" + d.nota));
