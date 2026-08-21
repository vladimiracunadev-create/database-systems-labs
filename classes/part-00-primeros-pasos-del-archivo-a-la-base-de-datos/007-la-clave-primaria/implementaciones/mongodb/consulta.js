// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/document/
// nota: el _id es obligatorio e INMUTABLE. Si se hubiera usado el correo como
//       _id, esta correccion no seria una actualizacion: habria que borrar el
//       documento y crear otro, con todo lo que apuntara a el.

// === preparacion ===
db.estudiantes.drop();
db.estudiantes.insertMany([
  { _id: 1, nombre: "Ada", correo: "ada@example.org" },
  { _id: 2, nombre: "Ada", correo: "ada2@example.org" },
  { _id: 3, nombre: "Linus", correo: "linus@example.org" },
]);
db.estudiantes.createIndex({ correo: 1 }, { unique: true });

db.estudiantes.updateOne({ _id: 2 }, { $set: { correo: "nuevo@example.org" } });

// === consulta ===
db.estudiantes
  .find()
  .sort({ _id: 1 })
  .forEach((d) => print(d._id + "|" + d.nombre + "|" + d.correo));
