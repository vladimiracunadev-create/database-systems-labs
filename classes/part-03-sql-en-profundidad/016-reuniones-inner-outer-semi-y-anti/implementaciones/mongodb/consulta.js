// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/reference/operator/aggregation/lookup/
// nota: $unwind con preserveNullAndEmptyArrays es lo que convierte el $lookup
//       en una reunion EXTERNA; sin esa opcion, Grace desaparece del resultado.

// === preparacion ===
db.estudiantes.drop();
db.cursos.drop();
db.inscripciones.drop();

db.estudiantes.insertMany([
  { _id: 1, nombre: "Ada" },
  { _id: 2, nombre: "Linus" },
  { _id: 3, nombre: "Grace" },
]);
db.cursos.insertMany([
  { _id: 10, codigo: "DB-101" },
  { _id: 20, codigo: "SE-201" },
]);
db.inscripciones.insertMany([
  { estudiante_id: 1, curso_id: 10 },
  { estudiante_id: 1, curso_id: 20 },
  { estudiante_id: 2, curso_id: 10 },
]);

// === consulta ===
db.estudiantes
  .aggregate([
    { $lookup: { from: "inscripciones", localField: "_id",
                 foreignField: "estudiante_id", as: "inscripcion" } },
    { $unwind: { path: "$inscripcion", preserveNullAndEmptyArrays: true } },
    { $lookup: { from: "cursos", localField: "inscripcion.curso_id",
                 foreignField: "_id", as: "curso" } },
    { $unwind: { path: "$curso", preserveNullAndEmptyArrays: true } },
    { $project: { _id: 0, nombre: 1,
                  codigo: { $ifNull: ["$curso.codigo", "sin-curso"] } } },
    { $sort: { nombre: 1, codigo: 1 } },
  ])
  .forEach((d) => print(d.nombre + "|" + d.codigo));
