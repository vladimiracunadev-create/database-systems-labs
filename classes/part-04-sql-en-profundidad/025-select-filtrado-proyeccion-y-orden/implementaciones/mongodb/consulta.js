// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/reference/method/cursor.sort/
// nota: el indice compuesto { curso: 1, nota: -1 } cubre el filtro Y el orden,
//       asi que el motor recorre el indice y se detiene en el segundo. Sin el,
//       la ordenacion en memoria esta limitada a 32 MB y la consulta falla.

// === preparacion ===
db.notas.drop();
db.notas.insertMany([
  { estudiante: "Ada", curso: "DB-101", nota: 90 },
  { estudiante: "Linus", curso: "DB-101", nota: 58 },
  { estudiante: "Grace", curso: "DB-101", nota: 72 },
  { estudiante: "Ada", curso: "SE-201", nota: 66 },
  { estudiante: "Grace", curso: "SE-201", nota: 78 },
]);
db.notas.createIndex({ curso: 1, nota: -1 });

// === consulta ===
db.notas
  .find({ curso: "DB-101", nota: { $gte: 60 } }, { _id: 0, estudiante: 1, nota: 1 })
  .sort({ nota: -1 })
  .limit(2)
  .forEach((d) => print(d.estudiante + "|" + d.nota));
