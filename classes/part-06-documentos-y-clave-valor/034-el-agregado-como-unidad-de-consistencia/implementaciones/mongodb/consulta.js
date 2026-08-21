// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/write-operations-atomicity/
// nota: aqui NO hay transaccion, y no hace falta. El pedido y sus lineas son un
//       solo documento, y la escritura de un documento es atomica: $push y $inc
//       en la misma orden se aplican juntos o no se aplica ninguno.

// === preparacion ===
db.pedidos.drop();

db.pedidos.insertOne({
  _id: "P-1",
  total: 200,
  lineas: [
    { producto: "teclado", importe: 120 },
    { producto: "raton", importe: 80 },
  ],
});

// Una sola orden: la linea nueva y el total suben juntos.
db.pedidos.updateOne(
  { _id: "P-1" },
  {
    $push: { lineas: { producto: "cable", importe: 100 } },
    $inc: { total: 100 },
  },
);

// === consulta ===
db.pedidos
  .aggregate([
    { $project: { _id: 0, pedido: "$_id", total_guardado: "$total",
                  total_calculado: { $sum: "$lineas.importe" } } },
    { $sort: { pedido: 1 } },
  ])
  .forEach((d) => print(d.pedido + "|" + d.total_guardado + "|" + d.total_calculado));
