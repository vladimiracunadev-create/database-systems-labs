// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/indexes/index-types/index-text/
// nota: solo se permite UN indice de texto por coleccion, y el idioma decide
//       las raices y las palabras vacias. La puntuacion se expone con
//       $meta: "textScore", y es rudimentaria comparada con BM25.

// === preparacion ===
db.documentos.drop();
db.documentos.insertMany([
  { _id: "d1", titulo: "Introduccion a las bases de datos relacionales" },
  { _id: "d2", titulo: "Bases de datos distribuidas y replicacion" },
  { _id: "d3", titulo: "Redes de computadores y protocolos" },
]);
db.documentos.createIndex({ titulo: "text" }, { default_language: "spanish" });

// === consulta ===
// Las comillas fuerzan que AMBOS terminos esten presentes; sin ellas, $text
// devuelve los documentos que tengan CUALQUIERA de los dos.
db.documentos
  .find({ $text: { $search: '"bases" "datos"' } }, { _id: 1 })
  .sort({ _id: 1 })
  .forEach((d) => print(d._id));
