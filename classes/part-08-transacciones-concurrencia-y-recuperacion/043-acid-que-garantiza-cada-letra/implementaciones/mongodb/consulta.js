// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/transactions/
// nota: implementacion DECLARADA, y el motivo es parte de la leccion: las
//       transacciones de varios documentos exigen un CONJUNTO DE REPLICAS. En
//       el servidor suelto que levanta este repositorio, este guion falla con
//       «Transaction numbers are only allowed on a replica set member or
//       mongos». No se ejecuta porque no se puede, y decirlo vale mas que
//       fingir que si.
//
//       Con una sola cuenta por documento no haria falta nada de esto: la
//       escritura de un documento ya es atomica. La transaccion aparece justo
//       cuando el agregado se reparte en dos documentos, que es la senal de que
//       el modelo documental se esta usando como si fuera relacional.

// === preparacion ===
db.cuentas.drop();
db.cuentas.insertMany([
  { _id: "A", saldo: 100 },
  { _id: "B", saldo: 50 },
]);

const sesion = db.getMongo().startSession();
const cuentas = sesion.getDatabase(db.getName()).cuentas;

// Transferencia valida.
sesion.startTransaction();
cuentas.updateOne({ _id: "A" }, { $inc: { saldo: -30 } });
cuentas.updateOne({ _id: "B" }, { $inc: { saldo: 30 } });
sesion.commitTransaction();

// Transferencia imposible: se comprueba DENTRO de la transaccion y se aborta.
sesion.startTransaction();
cuentas.updateOne({ _id: "B" }, { $inc: { saldo: 500 } });
const origen = cuentas.findOne({ _id: "A" });
if (origen.saldo < 500) {
  sesion.abortTransaction();
} else {
  cuentas.updateOne({ _id: "A" }, { $inc: { saldo: -500 } });
  sesion.commitTransaction();
}
sesion.endSession();

// === consulta ===
db.cuentas
  .find()
  .sort({ _id: 1 })
  .forEach((d) => print(d._id + "|" + d.saldo));
