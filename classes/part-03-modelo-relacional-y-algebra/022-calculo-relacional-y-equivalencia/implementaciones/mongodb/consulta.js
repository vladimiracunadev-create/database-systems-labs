// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/reference/operator/aggregation/setIsSubset/
// nota: sin cuantificadores, la unica via es la variante con agregacion:
//       recoger los cursos de cada estudiante y comprobar que el conjunto de
//       TODOS los cursos esta contenido en el suyo.

// === preparacion ===
db.cursos.drop();
db.inscripciones.drop();

db.cursos.insertMany([{ _id: "DB-101" }, { _id: "SE-201" }]);
db.inscripciones.insertMany([
  { estudiante: "Ada", curso: "DB-101" },
  { estudiante: "Ada", curso: "SE-201" },
  { estudiante: "Linus", curso: "DB-101" },
]);

// === consulta ===
const todos = db.cursos.find({}, { _id: 1 }).toArray().map((c) => c._id);
db.inscripciones
  .aggregate([
    { $group: { _id: "$estudiante", suyos: { $addToSet: "$curso" } } },
    { $match: { $expr: { $setIsSubset: [todos, "$suyos"] } } },
    { $sort: { _id: 1 } },
  ])
  .forEach((d) => print(d._id));
