// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/index-partial/
// nota: partialFilterExpression es el equivalente exacto del indice unico
//       parcial: el indice solo cubre los documentos que cumplen el filtro.

// === preparacion ===
db.clientes.drop();
db.direcciones.drop();

db.clientes.insertMany([
  { _id: 1, nombre: "Ada" },
  { _id: 2, nombre: "Linus" },
  { _id: 3, nombre: "Grace" },
]);

db.direcciones.createIndex(
  { cliente_id: 1 },
  { unique: true, partialFilterExpression: { principal: true } },
);

db.direcciones.insertMany([
  { cliente_id: 1, ciudad: "Santiago", principal: true },
  { cliente_id: 1, ciudad: "Valdivia", principal: false },
  { cliente_id: 2, ciudad: "Valparaiso", principal: true },
]);

try {
  db.direcciones.insertOne({ cliente_id: 1, ciudad: "Arica", principal: true });
} catch (e) {
  if (!String(e).includes("11000")) throw e;
}

// === consulta ===
db.clientes
  .aggregate([
    { $lookup: {
        from: "direcciones", let: { c: "$_id" },
        pipeline: [
          { $match: { $expr: { $and: [
            { $eq: ["$cliente_id", "$$c"] },
            { $eq: ["$principal", true] },
          ] } } },
        ],
        as: "principales" } },
    { $project: { _id: 0, cliente: "$nombre",
                  principales: { $size: "$principales" } } },
    { $sort: { cliente: 1 } },
  ])
  .forEach((d) => print(d.cliente + "|" + d.principales));
