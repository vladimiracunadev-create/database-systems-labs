// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/tutorial/equality-sort-range-guideline/
// nota: la regla tiene nombre propio en la documentacion de MongoDB —«igualdad,
//       orden, rango»— y es la misma de esta clase. Para medirla:
//         db.notas.find(...).explain("executionStats")
//       y comparar totalKeysExamined con nReturned: si el primero es mucho
//       mayor, el indice esta en mal orden.

// === preparacion ===
db.notas.drop();
db.notas.insertMany([
  { estudiante: "Ada", curso: "DB-101", nota: 90 },
  { estudiante: "Linus", curso: "DB-101", nota: 58 },
  { estudiante: "Grace", curso: "DB-101", nota: 72 },
  { estudiante: "Bob", curso: "DB-101", nota: 61 },
  { estudiante: "Ada", curso: "SE-201", nota: 66 },
  { estudiante: "Grace", curso: "SE-201", nota: 78 },
]);
db.notas.createIndex({ curso: 1, nota: 1 });

// === consulta ===
db.notas
  .find({ curso: "DB-101", nota: { $gte: 60, $lte: 90 } },
        { _id: 0, estudiante: 1, nota: 1 })
  .sort({ nota: 1, estudiante: 1 })
  .forEach((d) => print(d.estudiante + "|" + d.nota));
