// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/
// nota: $group por la pareja de campos hace de DISTINCT. El $sort explicito
//       deja claro que el orden se pide; no se hereda del orden de insercion.

// === preparacion ===
db.accesos.drop();
db.accesos.insertMany([
  { estudiante: "Linus", curso: "DB-101" },
  { estudiante: "Ada", curso: "DB-101" },
  { estudiante: "Ada", curso: "DB-101" },
  { estudiante: "Ada", curso: "SE-201" },
  { estudiante: "Linus", curso: "DB-101" },
]);

// === consulta ===
db.accesos
  .aggregate([
    { $group: { _id: { estudiante: "$estudiante", curso: "$curso" } } },
    { $sort: { "_id.estudiante": 1, "_id.curso": 1 } },
  ])
  .forEach((d) => print(d._id.estudiante + "|" + d._id.curso));
