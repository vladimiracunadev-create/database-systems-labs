// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/changeStreams/
// nota: la captura de cambios aqui son los FLUJOS DE CAMBIOS, con reanudacion
//       por testigo:
//         const flujo = db.destino.watch([], { resumeAfter: testigo });
//       Y su limite: el testigo caduca con el oplog. Si el consumidor esta
//       parado mas tiempo del que cubre el oplog, no puede reanudar y hay que
//       recargarlo todo. Dimensionar el oplog es parte del diseno.

// === preparacion ===
db.destino.drop();

const lote = [
  { cliente: "C-1", saldo: 10 },
  { cliente: "C-2", saldo: 20 },
  { cliente: "C-3", saldo: 30 },
];

function cargar(lote) {
  for (const fila of lote) {
    db.destino.updateOne(
      { _id: fila.cliente },
      { $set: { saldo: fila.saldo } },
      { upsert: true },
    );
  }
}

cargar(lote);
cargar(lote); // el mismo lote, otra vez

// === consulta ===
db.destino
  .find()
  .sort({ _id: 1 })
  .forEach((d) => print(d._id + "|" + d.saldo));
