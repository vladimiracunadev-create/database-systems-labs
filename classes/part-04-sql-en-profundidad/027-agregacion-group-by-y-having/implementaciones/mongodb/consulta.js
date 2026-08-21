// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/
// nota: aqui el doble conteo NO puede ocurrir: cada $lookup deja su propio
//       arreglo y $size cuenta cada uno por separado. El precio es que son dos
//       busquedas por curso, no una reunion.

// === preparacion ===
db.cursos.drop();
db.inscripciones.drop();
db.evaluaciones.drop();

db.cursos.insertMany([{ _id: "DB-101" }, { _id: "SE-201" }]);
db.inscripciones.insertMany([
  { estudiante: "Ada", curso: "DB-101" },
  { estudiante: "Linus", curso: "DB-101" },
  { estudiante: "Grace", curso: "SE-201" },
]);
db.evaluaciones.insertMany([
  { curso: "DB-101", titulo: "Control 1" },
  { curso: "DB-101", titulo: "Control 2" },
  { curso: "DB-101", titulo: "Examen" },
  { curso: "SE-201", titulo: "Examen" },
]);

// === consulta ===
db.cursos
  .aggregate([
    { $lookup: { from: "inscripciones", localField: "_id",
                 foreignField: "curso", as: "i" } },
    { $lookup: { from: "evaluaciones", localField: "_id",
                 foreignField: "curso", as: "e" } },
    { $project: { _id: 0, curso: "$_id",
                  inscritos: { $size: "$i" }, evaluaciones: { $size: "$e" } } },
    { $sort: { curso: 1 } },
  ])
  .forEach((d) => print(d.curso + "|" + d.inscritos + "|" + d.evaluaciones));
