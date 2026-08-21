// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/timeseries-collections/
// nota: una coleccion de series temporales agrupa internamente las medidas por
//       metaField y ventana de tiempo. El metaField hace el papel de la clave
//       de particion de Cassandra, y elegirlo mal produce el mismo problema:
//       un fragmento que recibe toda la escritura.

// === preparacion ===
db.lecturas.drop();
db.createCollection("lecturas", {
  timeseries: { timeField: "momento", metaField: "dispositivo", granularity: "minutes" },
});
db.lecturas.insertMany([
  { dispositivo: "sensor-1", momento: new Date("2026-08-19T10:00:00Z"), valor: 21 },
  { dispositivo: "sensor-1", momento: new Date("2026-08-19T10:01:00Z"), valor: 22 },
  { dispositivo: "sensor-1", momento: new Date("2026-08-19T10:02:00Z"), valor: 23 },
  { dispositivo: "sensor-2", momento: new Date("2026-08-19T10:00:00Z"), valor: 30 },
  { dispositivo: "sensor-2", momento: new Date("2026-08-19T10:01:00Z"), valor: 31 },
]);

// === consulta ===
db.lecturas
  .find({ dispositivo: "sensor-1" })
  .sort({ momento: -1 })
  .limit(2)
  .forEach((d) => print(d.momento.toISOString().replace(".000Z", "Z") + "|" + d.valor));
