// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/write-operations-atomicity/
// nota: el registro de la saga cabe en un documento por operacion, con los
//       pasos dentro. Escribir un paso es una escritura atomica: ni transaccion
//       ni conjunto de replicas. Lo que NO garantiza nada es que el estado
//       escrito aqui coincida con el mundo real: si el servicio de vuelos no
//       recibio la cancelacion, el documento dira 'compensado' igualmente.

// === preparacion ===
db.sagas.drop();
db.sagas.insertOne({ _id: "reserva-42", pasos: [] });

// Paso 1: el vuelo se confirma de verdad, en otro sistema.
db.sagas.updateOne(
  { _id: "reserva-42" },
  { $push: { pasos: { paso: "vuelo", estado: "confirmado" } } },
);

// Paso 2: el hotel falla.
db.sagas.updateOne(
  { _id: "reserva-42" },
  { $push: { pasos: { paso: "hotel", estado: "fallido" } } },
);

// Compensacion: accion inversa sobre el paso ya confirmado.
db.sagas.updateOne(
  { _id: "reserva-42", "pasos.paso": "vuelo" },
  { $set: { "pasos.$.estado": "compensado" } },
);

// === consulta ===
db.sagas
  .aggregate([
    { $unwind: "$pasos" },
    { $project: { _id: 0, paso: "$pasos.paso", estado: "$pasos.estado" } },
    { $sort: { paso: 1 } },
  ])
  .forEach((d) => print(d.paso + "|" + d.estado));
