// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/reference/operator/aggregation/inc/
// nota: $inc es atomico sobre UN documento. La inscripcion y el contador viven
//       en documentos distintos, asi que mantenerlos de acuerdo ante un fallo
//       exige una transaccion de varios documentos; aqui se escribe la version
//       simple y se declara el riesgo, que es la unica forma honesta.

// === preparacion ===
db.cursos.drop();
db.inscripciones.drop();

db.cursos.insertMany([
  { _id: 10, codigo: "DB-101", inscritos: 0 },
  { _id: 20, codigo: "SE-201", inscritos: 0 },
]);

function inscribir(estudiante, cursoId) {
  db.inscripciones.insertOne({ estudiante: estudiante, curso_id: cursoId });
  db.cursos.updateOne({ _id: cursoId }, { $inc: { inscritos: 1 } });
}
function darDeBaja(estudiante, cursoId) {
  db.inscripciones.deleteOne({ estudiante: estudiante, curso_id: cursoId });
  db.cursos.updateOne({ _id: cursoId }, { $inc: { inscritos: -1 } });
}

inscribir("Ada", 10);
inscribir("Linus", 10);
inscribir("Grace", 20);
inscribir("Bob", 20);
darDeBaja("Bob", 20);

// === consulta ===
db.cursos
  .aggregate([
    { $lookup: { from: "inscripciones", localField: "_id",
                 foreignField: "curso_id", as: "i" } },
    { $project: { _id: 0, curso: "$codigo", contador: "$inscritos",
                  calculado: { $size: "$i" } } },
    { $sort: { curso: 1 } },
  ])
  .forEach((d) => print(d.curso + "|" + d.contador + "|" + d.calculado));
