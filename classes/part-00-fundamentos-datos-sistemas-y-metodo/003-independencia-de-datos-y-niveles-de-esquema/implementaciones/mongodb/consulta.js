// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/views/
// nota: una vista es una tuberia de agregacion con nombre. Aqui el cambio
//       fisico es el mismo: el estado deja de ser una cadena repetida y pasa a
//       ser un codigo con su coleccion de referencia.

// === preparacion ===
db.panel_inscripciones.drop();
db.inscripciones_v1.drop();
db.inscripciones_v2.drop();
db.estados.drop();

// 1. Esquema de partida.
db.inscripciones_v1.insertMany([
  { estudiante: "Ada", estado: "activa" },
  { estudiante: "Linus", estado: "completada" },
  { estudiante: "Grace", estado: "retirada" },
]);

// 2. Esquema externo: lo unico que la aplicacion conoce.
db.createView("panel_inscripciones", "inscripciones_v1", [
  { $project: { _id: 0, estudiante: 1, estado: 1 } },
]);

// 3. Reorganizacion fisica.
db.estados.insertMany([
  { _id: 1, nombre: "activa" },
  { _id: 2, nombre: "completada" },
  { _id: 3, nombre: "retirada" },
]);
db.inscripciones_v2.insertMany([
  { estudiante: "Ada", estado_codigo: 1 },
  { estudiante: "Linus", estado_codigo: 2 },
  { estudiante: "Grace", estado_codigo: 3 },
]);

// 4. La vista absorbe el cambio.
db.panel_inscripciones.drop();
db.inscripciones_v1.drop();
db.createView("panel_inscripciones", "inscripciones_v2", [
  { $lookup: { from: "estados", localField: "estado_codigo",
               foreignField: "_id", as: "e" } },
  { $unwind: "$e" },
  { $project: { _id: 0, estudiante: 1, estado: "$e.nombre" } },
]);

// === consulta ===
// La misma consulta de siempre, contra el mismo nombre de siempre.
db.panel_inscripciones
  .find()
  .sort({ estudiante: 1 })
  .forEach((d) => print(d.estudiante + "|" + d.estado));
