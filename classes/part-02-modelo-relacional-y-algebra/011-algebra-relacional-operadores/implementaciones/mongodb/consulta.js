// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/aggregation-pipeline-optimization/
// nota: la tuberia ES la expresion algebraica escrita en orden. El $match va
//       PRIMERO a proposito: es el empuje del filtro hecho a mano.

// === preparacion ===
db.estudiantes.drop();
db.notas.drop();

db.estudiantes.insertMany([
  { _id: 1, nombre: "Ada" },
  { _id: 2, nombre: "Linus" },
  { _id: 3, nombre: "Grace" },
]);
db.notas.insertMany([
  { estudiante_id: 1, curso: "DB-101", nota: 90 },
  { estudiante_id: 2, curso: "DB-101", nota: 58 },
  { estudiante_id: 3, curso: "DB-101", nota: 72 },
  { estudiante_id: 1, curso: "SE-201", nota: 66 },
  { estudiante_id: 3, curso: "SE-201", nota: 78 },
]);

// === consulta ===
db.notas
  .aggregate([
    { $match: { curso: "DB-101", nota: { $gte: 60 } } },
    { $lookup: { from: "estudiantes", localField: "estudiante_id",
                 foreignField: "_id", as: "e" } },
    { $unwind: "$e" },
    { $project: { _id: 0, nombre: "$e.nombre", nota: 1 } },
    { $sort: { nombre: 1 } },
  ])
  .forEach((d) => print(d.nombre + "|" + d.nota));
