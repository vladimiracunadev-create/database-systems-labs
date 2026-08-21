// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/reference/bson-type-comparison-order/
// nota: BSON distingue int, long, double y decimal, y ordena por valor
//       numerico. La trampa es otra: el tipo lo decide CADA documento. Si un
//       precio se guarda como "80" y otro como 80, el orden mezcla dos
//       criterios segun una precedencia de tipos que casi nadie conoce.
//       Y en mongosh, 80 es un DOUBLE salvo que se escriba NumberInt(80).

// === preparacion ===
db.productos.drop();
db.productos.insertMany([
  { _id: "teclado", precio: NumberInt(120) },
  { _id: "raton", precio: NumberInt(80) },
  { _id: "cable", precio: NumberInt(100) },
]);

// === consulta ===
db.productos
  .find()
  .sort({ precio: 1 })
  .forEach((d) => print(d._id + "|" + d.precio));
