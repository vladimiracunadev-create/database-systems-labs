// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/schema-validation/
// nota: la validacion es OPCIONAL y hay que pedirla. Con validationAction "warn"
//       el documento invalido se guardaria igual y solo quedaria una linea en un
//       registro que nadie lee. Y se aplica solo a las escrituras POSTERIORES:
//       lo que ya estaba mal, sigue mal.

// === preparacion ===
db.notas.drop();
db.createCollection("notas", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["estudiante", "nota"],
      properties: {
        estudiante: { bsonType: "string" },
        nota: { bsonType: "int", minimum: 0, maximum: 100 },
      },
    },
  },
  validationAction: "error",
});

db.notas.insertOne({ estudiante: "Ada", nota: NumberInt(90) });
db.notas.insertOne({ estudiante: "Linus", nota: NumberInt(58) });
db.notas.insertOne({ estudiante: "Grace", nota: NumberInt(72) });

let rechazado = false;
try {
  db.notas.insertOne({ estudiante: "Bob", nota: NumberInt(130) });
} catch (e) {
  rechazado = true;
}
if (!rechazado) throw new Error("el validador acepto una nota de 130 sobre 100");

// === consulta ===
db.notas
  .find({}, { _id: 0, estudiante: 1, nota: 1 })
  .sort({ estudiante: 1 })
  .forEach((d) => print(d.estudiante + "|" + d.nota));
