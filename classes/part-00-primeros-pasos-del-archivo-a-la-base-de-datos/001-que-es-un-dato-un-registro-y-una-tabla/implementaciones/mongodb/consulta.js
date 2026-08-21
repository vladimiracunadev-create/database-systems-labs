// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/document/
// nota: aqui no se declara ninguna estructura antes de escribir. Es comodo, y
//       tiene precio: nada impide que el documento siguiente traiga otros
//       campos o el curso escrito de otra forma.

// === preparacion ===
db.inscripciones.drop();
db.inscripciones.insertMany([
  { estudiante: "Ada", curso: "DB-101" },
  { estudiante: "Ada", curso: "SE-201" },
  { estudiante: "Linus", curso: "DB-101" },
]);

// === consulta ===
db.inscripciones
  .find({}, { _id: 0, estudiante: 1, curso: 1 })
  .sort({ estudiante: 1, curso: 1 })
  .forEach((d) => print(d.estudiante + "|" + d.curso));
