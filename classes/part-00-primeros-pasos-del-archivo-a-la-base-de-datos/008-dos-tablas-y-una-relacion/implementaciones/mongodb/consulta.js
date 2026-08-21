// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/
// nota: el mismo modelo con referencias, y la diferencia que importa: NO HAY
//       CLAVES FORANEAS. Esto se acepta sin protestar:
//         db.inscripciones.insertOne({ estudiante_id: 99, curso_id: 10 })
//       y ninguna consulta avisa: la inscripcion huerfana simplemente no
//       aparece en el $lookup, como si no existiera.

// === preparacion ===
db.estudiantes.drop();
db.cursos.drop();
db.inscripciones.drop();

db.estudiantes.insertMany([
  { _id: 1, nombre: "Ada" },
  { _id: 2, nombre: "Linus" },
]);
db.cursos.insertMany([
  { _id: 10, codigo: "DB-101", profesor: "A. Lovelace" },
  { _id: 20, codigo: "SE-201", profesor: "G. Hopper" },
]);
db.inscripciones.insertMany([
  { estudiante_id: 1, curso_id: 10 },
  { estudiante_id: 1, curso_id: 20 },
  { estudiante_id: 2, curso_id: 10 },
]);

// === consulta ===
db.inscripciones
  .aggregate([
    { $lookup: { from: "estudiantes", localField: "estudiante_id",
                 foreignField: "_id", as: "e" } },
    { $lookup: { from: "cursos", localField: "curso_id",
                 foreignField: "_id", as: "c" } },
    { $unwind: "$e" },
    { $unwind: "$c" },
    { $project: { _id: 0, nombre: "$e.nombre", codigo: "$c.codigo",
                  profesor: "$c.profesor" } },
    { $sort: { nombre: 1, codigo: 1 } },
  ])
  .forEach((d) => print(d.nombre + "|" + d.codigo + "|" + d.profesor));
