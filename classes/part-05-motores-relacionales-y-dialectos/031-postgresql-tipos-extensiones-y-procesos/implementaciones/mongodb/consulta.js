// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/indexes/index-types/index-multikey/
// nota: el indice sobre un campo de arreglo es MULTICLAVE: crea una entrada por
//       elemento. Es lo que hace que { etiquetas: "datos" } sea una busqueda
//       indexada y no un recorrido.

// === preparacion ===
db.cursos.drop();
db.cursos.insertMany([
  { _id: "DB-101", etiquetas: ["sql", "datos"] },
  { _id: "SE-201", etiquetas: ["proceso"] },
  { _id: "AR-301", etiquetas: ["datos", "diseno"] },
]);
db.cursos.createIndex({ etiquetas: 1 });

// === consulta ===
db.cursos
  .find({ etiquetas: "datos" }, { _id: 1 })
  .sort({ _id: 1 })
  .forEach((d) => print(d._id));
