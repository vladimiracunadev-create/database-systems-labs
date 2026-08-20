// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/document/
// nota: el _id es inmutable. Si se hubiera usado el correo como _id, este
//       cambio no seria un update: seria borrar el documento y crear otro.

// === preparacion ===
db.estudiantes.drop();
db.inscripciones.drop();

db.estudiantes.insertMany([
  { _id: 1, correo: "ada@example.org" },
  { _id: 2, correo: "linus@example.org" },
  { _id: 3, correo: "grace@example.org" },
]);
db.estudiantes.createIndex({ correo: 1 }, { unique: true });
db.inscripciones.insertMany([
  { estudiante_id: 1, curso: "DB-101" },
  { estudiante_id: 1, curso: "SE-201" },
  { estudiante_id: 2, curso: "DB-101" },
]);

// Una sola escritura, y ninguna inscripcion se entera.
db.estudiantes.updateOne({ _id: 1 }, { $set: { correo: "ada@nuevo.org" } });

// === consulta ===
db.estudiantes
  .aggregate([
    { $lookup: { from: "inscripciones", localField: "_id",
                 foreignField: "estudiante_id", as: "i" } },
    { $project: { _id: 0, correo: 1, inscripciones: { $size: "$i" } } },
    { $sort: { correo: 1 } },
  ])
  .forEach((d) => print(d.correo + "|" + d.inscripciones));
