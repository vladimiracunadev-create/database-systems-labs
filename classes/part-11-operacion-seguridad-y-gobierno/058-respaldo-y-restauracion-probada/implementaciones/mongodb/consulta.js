// motor: mongodb
// doc: https://www.mongodb.com/docs/database-tools/mongodump/
// nota: mongodump sobre un conjunto de replicas NO da una copia coherente entre
//       colecciones salvo que se use --oplog, y sobre un cluster fragmentado
//       hay que detener el balanceador. Son detalles que solo se descubren
//       restaurando, y por eso hay que restaurar antes del incidente.

// === preparacion ===
db.notas.drop();
db.notas_restauradas.drop();

db.notas.insertMany([
  { _id: 1, estudiante: "Ada", nota: 90 },
  { _id: 2, estudiante: "Ada", nota: 58 },
  { _id: 3, estudiante: "Linus", nota: 78 },
  { _id: 4, estudiante: "Linus", nota: 66 },
  { _id: 5, estudiante: "Grace", nota: 55 },
  { _id: 6, estudiante: "Grace", nota: 55 },
]);

// La «restauracion»: aqui, una copia de la coleccion.
db.notas.aggregate([{ $out: "notas_restauradas" }]).toArray();

// === consulta ===
for (const [nombre, coleccion] of [["origen", db.notas],
                                   ["restaurado", db.notas_restauradas]]) {
  const r = coleccion
    .aggregate([{ $group: { _id: null, filas: { $sum: 1 }, suma: { $sum: "$nota" } } }])
    .toArray()[0];
  print(nombre + "|" + r.filas + "|" + r.suma);
}
