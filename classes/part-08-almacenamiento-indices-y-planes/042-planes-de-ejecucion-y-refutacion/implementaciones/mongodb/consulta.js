// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/reference/explain-results/
// nota: como se mide aqui:
//         db.estudiantes.aggregate([...]).explain("executionStats")
//       Las tres cifras que resuelven casi todo:
//         nReturned            lo que devolvio
//         totalKeysExamined    entradas de indice leidas
//         totalDocsExamined    documentos leidos
//       Si los dos ultimos son mucho mayores que el primero, se lee de mas.
//       Y recordar que el plan ganador queda CACHEADO: la consulta puede
//       degradarse meses despues sin que el codigo haya cambiado.

// === preparacion ===
db.estudiantes.drop();
db.inscripciones.drop();
db.estudiantes.insertMany([
  { _id: "Ada" }, { _id: "Linus" }, { _id: "Grace" },
]);
db.inscripciones.insertMany([
  { estudiante: "Ada", curso: "DB-101" },
  { estudiante: "Ada", curso: "SE-201" },
  { estudiante: "Linus", curso: "DB-101" },
]);
db.inscripciones.createIndex({ estudiante: 1 });

// === consulta ===
// La forma barata: agrupar por estudiante en la coleccion PEQUENA de las
// inscripciones, en vez de recorrer los estudiantes buscando cada uno.
db.inscripciones
  .aggregate([
    { $group: { _id: "$estudiante" } },
    { $sort: { _id: 1 } },
  ])
  .forEach((d) => print(d._id));
