// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/index-ttl/
// nota: el indice TTL es la forma mas dificil de OLVIDAR una politica de
//       retencion: se declara una vez y el motor borra. Y el aviso: borra por
//       documento, compite con la carga normal, no devuelve el espacio hasta
//       compactar, y si se configura mal borra lo que no debia sin papelera.

// === preparacion ===
db.eventos.drop();
db.eventos.insertMany([
  { _id: 1, correo: "ada@example.org", fecha: new Date("2025-01-15") },
  { _id: 2, correo: "linus@example.org", fecha: new Date("2026-08-10") },
  { _id: 3, correo: "grace@otro.org", fecha: new Date("2026-08-15") },
]);

// Retencion explicita (el indice TTL haria lo mismo sin que nadie lo pida):
db.eventos.deleteMany({ fecha: { $lt: new Date("2026-01-01") } });

// === consulta ===
db.eventos
  .aggregate([
    { $project: {
        _id: 0,
        correo: { $concat: ["***@", { $arrayElemAt: [{ $split: ["$correo", "@"] }, 1] }] },
        fecha: { $dateToString: { format: "%Y-%m-%d", date: "$fecha" } } } },
    { $sort: { fecha: 1 } },
  ])
  .forEach((d) => print(d.correo + "|" + d.fecha));
