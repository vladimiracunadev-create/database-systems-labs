// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/reference/method/db.collection.updateOne/
// nota: matchedCount es la senal. Si vale 0, otro cliente se adelanto y hay que
//       releer y reintentar. La version hay que incrementarla en CADA camino de
//       escritura: si uno solo la olvida, la proteccion desaparece para todos.

// === preparacion ===
db.cuentas.drop();
db.cuentas.insertOne({ _id: "cuenta-1", saldo: 100, version: 1 });

// Cliente A: leyo version 1.
const a = db.cuentas.updateOne(
  { _id: "cuenta-1", version: 1 },
  { $inc: { saldo: -30, version: 1 } },
);

// Cliente B: leyo TAMBIEN la version 1.
const b = db.cuentas.updateOne(
  { _id: "cuenta-1", version: 1 },
  { $inc: { saldo: -50, version: 1 } },
);

if (a.matchedCount !== 1 || b.matchedCount !== 0) {
  throw new Error("el bloqueo optimista no actuo como debia");
}

// === consulta ===
db.cuentas
  .find()
  .sort({ _id: 1 })
  .forEach((d) => print(d._id + "|" + d.saldo + "|" + d.version));
