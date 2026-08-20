// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/reference/operator/aggregation/group/
// nota: $group sin _id agrega sobre toda la coleccion. Los enteros de mongosh
//       son de doble precision salvo que se use NumberInt o NumberDecimal: por
//       eso las notas se escriben como enteros exactos y no como decimales.

// === preparacion ===
db.notas.drop();
db.notas.insertMany([
  { _id: 1, estudiante: "Ada", nota: NumberInt(90) },
  { _id: 2, estudiante: "Ada", nota: NumberInt(58) },
  { _id: 3, estudiante: "Linus", nota: NumberInt(78) },
  { _id: 4, estudiante: "Linus", nota: NumberInt(66) },
  { _id: 5, estudiante: "Grace", nota: NumberInt(55) },
  { _id: 6, estudiante: "Grace", nota: NumberInt(55) },
]);

// === consulta ===
db.notas
  .aggregate([
    { $group: { _id: null, filas: { $sum: 1 }, suma_notas: { $sum: "$nota" } } },
  ])
  .forEach((d) => print(d.filas + "|" + d.suma_notas));
