// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/index-ttl/
// nota: el indice TTL libera ESPACIO, no define VISIBILIDAD: el proceso que
//       borra corre cada 60 segundos, asi que un documento vencido sigue
//       siendo visible hasta un minuto despues. La consulta filtra por fecha
//       igualmente; el indice solo evita que la coleccion crezca sin fin.

// === preparacion ===
db.cache.drop();
db.cache.createIndex({ expira_en: 1 }, { expireAfterSeconds: 0 });

db.cache.insertMany([
  { _id: "k1", valor: "con caducidad", expira_en: new Date("2099-01-01T00:00:00Z") },
  { _id: "k2", valor: "permanente" },
]);
// k3 no se inserta.

// === consulta ===
for (const clave of ["k1", "k2", "k3"]) {
  const doc = db.cache.findOne({ _id: clave });
  const estado = doc === null
    ? "ausente"
    : doc.expira_en === undefined
      ? "permanente"
      : "expira";
  print(clave + "|" + estado);
}
