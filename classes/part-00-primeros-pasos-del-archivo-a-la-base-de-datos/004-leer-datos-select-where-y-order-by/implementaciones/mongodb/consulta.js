// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/reference/method/cursor.sort/
// nota: las mismas tres decisiones con otra sintaxis: el primer argumento de
//       find() es el WHERE, el segundo es el SELECT, y sort() es el ORDER BY.

// === preparacion ===
db.notas.drop();
db.notas.insertMany([
  { estudiante: "Ada", curso: "DB-101", nota: 90 },
  { estudiante: "Linus", curso: "DB-101", nota: 58 },
  { estudiante: "Grace", curso: "DB-101", nota: 72 },
  { estudiante: "Ada", curso: "SE-201", nota: 66 },
]);

// === consulta ===
db.notas
  .find({ curso: "DB-101", nota: { $gte: 60 } }, { _id: 0, estudiante: 1, nota: 1 })
  .sort({ estudiante: 1 })
  .forEach((d) => print(d.estudiante + "|" + d.nota));
