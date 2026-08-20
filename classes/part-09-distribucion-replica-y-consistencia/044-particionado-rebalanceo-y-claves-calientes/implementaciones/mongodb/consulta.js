// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/sharding-shard-key/
// nota: en un cluster fragmentado, esta misma agregacion sobre la coleccion
//       config.chunks dice cuantos trozos tiene cada fragmento. Y la trampa que
//       no se ve aqui: una clave MONOTONA —una fecha, un contador— manda todas
//       las escrituras al mismo fragmento, aunque el reparto de datos parezca
//       equilibrado.

// === preparacion ===
db.pedidos.drop();
db.pedidos.insertMany([
  { _id: 1, cliente: "A" }, { _id: 2, cliente: "A" }, { _id: 3, cliente: "A" },
  { _id: 4, cliente: "A" }, { _id: 5, cliente: "A" }, { _id: 6, cliente: "A" },
  { _id: 7, cliente: "A" }, { _id: 8, cliente: "A" }, { _id: 9, cliente: "B" },
  { _id: 10, cliente: "C" },
]);

// === consulta ===
db.pedidos
  .aggregate([
    { $group: { _id: "$cliente", pedidos: { $sum: 1 } } },
    { $sort: { pedidos: -1, _id: 1 } },
  ])
  .forEach((d) => print(d._id + "|" + d.pedidos));
