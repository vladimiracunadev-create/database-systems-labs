// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/reference/operator/query/type/
// nota: la trampa aqui es otra. { estudiante: null } encuentra TANTO los
//       documentos con el campo en null COMO los que no tienen el campo. Para
//       distinguirlos hay que usar { estudiante: { $type: "null" } } frente a
//       { estudiante: { $exists: false } }.

// === preparacion ===
db.estudiantes.drop();
db.inscripciones.drop();

db.estudiantes.insertMany([
  { nombre: "Ada" },
  { nombre: "Linus" },
  { nombre: "Grace" },
]);
db.inscripciones.insertMany([
  { estudiante: "Ada", curso: "DB-101" },
  { estudiante: "Linus", curso: "DB-101" },
  { estudiante: null, curso: "SE-201" },
]);

// === consulta ===
db.estudiantes
  .aggregate([
    { $lookup: { from: "inscripciones", localField: "nombre",
                 foreignField: "estudiante", as: "i" } },
    { $match: { i: { $size: 0 } } },
    { $project: { _id: 0, nombre: 1 } },
    { $sort: { nombre: 1 } },
  ])
  .forEach((d) => print(d.nombre));
