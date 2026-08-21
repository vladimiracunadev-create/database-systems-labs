// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/data-modeling/schema-design-process/
// nota: la fase de EXPANDIR es gratis: anadir un campo es escribir documentos
//       con el. Lo que no es gratis es lo de despues: el codigo tiene que
//       tratar con documentos viejos SIN el campo y nuevos con el, a veces
//       durante anos. La migracion no desaparece, se vuelve invisible.

// === preparacion ===
db.personas.drop();
db.personas.insertMany([
  { _id: 1, nombre: "Ada Lovelace" },
  { _id: 2, nombre: "Linus Torvalds" },
]);

// MIGRAR: por lotes, sin bloquear nada.
db.personas.updateOne({ _id: 1 }, { $set: { apellido: "Lovelace" } });
db.personas.updateOne({ _id: 2 }, { $set: { apellido: "Torvalds" } });

// La version nueva del codigo ya escribe las dos cosas.
db.personas.insertOne({ _id: 3, nombre: "Grace Hopper", apellido: "Hopper" });

// CONTRAER seria, aqui, un validador $jsonSchema que exija el campo. Y solo
// cuando ya no queden documentos sin el:
//   db.personas.countDocuments({ apellido: { $exists: false } })  ->  0

// === consulta ===
db.personas
  .find({}, { _id: 1, apellido: 1 })
  .sort({ _id: 1 })
  .forEach((d) => print(d._id + "|" + d.apellido));
