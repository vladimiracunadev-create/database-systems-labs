// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/data-modeling/concepts/embedding-vs-references/
// nota: forma INCRUSTADA. Un documento, un viaje, sin reunion. La forma
//       referenciada seria una coleccion `lineas` con `pedido_id` y un $lookup:
//       correcta cuando las lineas crecen sin techo o se consultan solas.

// === preparacion ===
db.pedidos.drop();
db.pedidos.insertOne({
  _id: "P-1",
  lineas: [
    { producto: "teclado", importe: 120 },
    { producto: "raton", importe: 80 },
    { producto: "cable", importe: 100 },
  ],
});

// === consulta ===
db.pedidos
  .aggregate([
    { $match: { _id: "P-1" } },
    { $unwind: "$lineas" },
    { $project: { _id: 0, producto: "$lineas.producto", importe: "$lineas.importe" } },
    { $sort: { producto: 1 } },
  ])
  .forEach((d) => print(d.producto + "|" + d.importe));
