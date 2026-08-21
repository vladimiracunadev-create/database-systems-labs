// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/aggregation-pipeline/
// nota: el indice multiclave sobre lineas.categoria acelera el FILTRO, no el
//       $group: agrupar siempre recorre los documentos que pasen el filtro, con
//       un limite de 100 MB por etapa salvo que se permita usar disco.

// === preparacion ===
db.pedidos.drop();
db.pedidos.insertMany([
  { _id: "P-1", lineas: [
    { producto: "teclado", categoria: "perifericos", importe: 120 },
    { producto: "raton", categoria: "accesorios", importe: 80 },
  ] },
  { _id: "P-2", lineas: [
    { producto: "cable", categoria: "accesorios", importe: 100 },
  ] },
]);
db.pedidos.createIndex({ "lineas.categoria": 1 });

// === consulta ===
db.pedidos
  .aggregate([
    { $unwind: "$lineas" },
    { $group: { _id: "$lineas.categoria", importe: { $sum: "$lineas.importe" } } },
    { $sort: { _id: 1 } },
  ])
  .forEach((d) => print(d._id + "|" + d.importe));
