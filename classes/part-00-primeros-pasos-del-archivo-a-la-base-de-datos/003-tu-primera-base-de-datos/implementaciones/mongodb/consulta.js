// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/reference/method/db.collection.insertMany/
// nota: no hay CREATE. Insertar un documento crea la coleccion, y cada
//       documento puede tener campos distintos. Grace no lleva el campo correo:
//       en una tabla habria una celda vacia, aqui no hay celda.

// === preparacion ===
db.estudiantes.drop();
db.estudiantes.insertMany([
  { _id: 1, nombre: "Ada", correo: "ada@example.org" },
  { _id: 2, nombre: "Linus", correo: "linus@example.org" },
  { _id: 3, nombre: "Grace" },
]);

// === consulta ===
db.estudiantes
  .find({}, { _id: 1, nombre: 1 })
  .sort({ nombre: 1 })
  .forEach((d) => print(d._id + "|" + d.nombre));
