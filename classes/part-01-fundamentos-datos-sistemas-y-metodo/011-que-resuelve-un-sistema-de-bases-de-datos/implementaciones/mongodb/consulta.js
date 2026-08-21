// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/index-unique/
// nota: con ordered:false, insertMany intenta TODOS los documentos y solo
//       falla el que viola el indice; el try/catch recoge ese error concreto.

// === preparacion ===
db.estudiantes.drop();
db.estudiantes.createIndex({ correo: 1 }, { unique: true });

try {
  db.estudiantes.insertMany(
    [
      { _id: 1, correo: "ada@example.org" },
      { _id: 2, correo: "linus@example.org" },
      { _id: 3, correo: "ada@example.org" },
    ],
    { ordered: false },
  );
} catch (e) {
  // Error 11000 = clave duplicada. Es el resultado esperado, no un fallo.
  if (!String(e).includes("11000")) throw e;
}

// === consulta ===
db.estudiantes
  .find({}, { _id: 0, correo: 1 })
  .sort({ correo: 1 })
  .forEach((d) => print(d.correo));
