// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/index-partial/
// nota: el indice parcial solo se usa si la consulta INCLUYE su predicado. Si
//       la consulta pidiera { estado: { $in: ["pendiente", "enviado"] } }, el
//       motor no puede demostrar que implica el filtro del indice y lo ignora
//       en silencio: no hay aviso, solo una consulta mas lenta.

// === preparacion ===
db.pedidos.drop();
db.pedidos.insertMany([
  { _id: "P-1", estado: "entregado", fecha: "2026-08-01" },
  { _id: "P-2", estado: "pendiente", fecha: "2026-08-02" },
  { _id: "P-3", estado: "entregado", fecha: "2026-08-03" },
  { _id: "P-4", estado: "entregado", fecha: "2026-08-04" },
  { _id: "P-5", estado: "pendiente", fecha: "2026-08-05" },
  { _id: "P-6", estado: "entregado", fecha: "2026-08-06" },
]);
db.pedidos.createIndex(
  { fecha: 1 },
  { partialFilterExpression: { estado: "pendiente" } },
);

// === consulta ===
db.pedidos
  .find({ estado: "pendiente" }, { _id: 1, fecha: 1 })
  .sort({ fecha: 1 })
  .forEach((d) => print(d._id + "|" + d.fecha));
