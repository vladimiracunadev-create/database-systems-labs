// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/
// nota: modelo normalizado A PROPOSITO. Es lo correcto cuando el dato
//       referenciado cambia y lo comparten muchos documentos; si el nombre del
//       profesor estuviera incrustado en cada inscripcion, este updateOne
//       tendria que ser un updateMany sobre miles de documentos.

// === preparacion ===
db.profesores.drop();
db.cursos.drop();
db.inscripciones.drop();

db.profesores.insertMany([
  { _id: 1, nombre: "A. Lovelace" },
  { _id: 2, nombre: "Grace Hopper" },
]);
db.cursos.insertMany([
  { _id: 10, codigo: "DB-101", profesor_id: 1 },
  { _id: 20, codigo: "SE-201", profesor_id: 2 },
]);
db.inscripciones.insertMany([
  { estudiante: "Ada", curso_id: 10 },
  { estudiante: "Linus", curso_id: 10 },
  { estudiante: "Grace", curso_id: 20 },
]);

db.profesores.updateOne({ _id: 1 }, { $set: { nombre: "Ada Lovelace" } });

// === consulta ===
db.cursos
  .aggregate([
    { $lookup: { from: "profesores", localField: "profesor_id",
                 foreignField: "_id", as: "p" } },
    { $unwind: "$p" },
    { $lookup: { from: "inscripciones", localField: "_id",
                 foreignField: "curso_id", as: "i" } },
    { $project: { _id: 0, curso: "$codigo", profesor: "$p.nombre",
                  inscripciones: { $size: "$i" } } },
    { $sort: { curso: 1 } },
  ])
  .forEach((d) => print(d.curso + "|" + d.profesor + "|" + d.inscripciones));
