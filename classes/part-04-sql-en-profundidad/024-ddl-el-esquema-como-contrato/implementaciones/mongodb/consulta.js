// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/schema-validation/
// nota: validationAction "error" es lo que convierte el esquema en contrato.
//       Con "warn" el documento invalido se guarda igual y solo queda una
//       linea en el registro que nadie lee.

// === preparacion ===
db.notas.drop();
db.createCollection("notas", {
  validator: {
    $jsonSchema: {
      bsonType: "object",
      required: ["estudiante", "curso", "nota"],
      properties: {
        estudiante: { bsonType: "string", minLength: 1 },
        curso: { bsonType: "string" },
        nota: { bsonType: "int", minimum: 0, maximum: 100 },
      },
    },
  },
  validationAction: "error",
  validationLevel: "strict",
});

db.notas.insertOne({ estudiante: "Ada", curso: "DB-101", nota: NumberInt(90) });
db.notas.insertOne({ estudiante: "Linus", curso: "DB-101", nota: NumberInt(58) });

let rechazadas = 0;
for (const malo of [
  { estudiante: "Grace", curso: "DB-101", nota: NumberInt(130) },
  { estudiante: "", curso: "DB-101", nota: NumberInt(70) },
]) {
  try {
    db.notas.insertOne(malo);
  } catch (e) {
    rechazadas += 1;
  }
}
if (rechazadas !== 2) throw new Error("el validador acepto lo que prohibe");

// === consulta ===
db.notas
  .find({}, { _id: 0, estudiante: 1, nota: 1 })
  .sort({ estudiante: 1 })
  .forEach((d) => print(d.estudiante + "|" + d.nota));
