// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/reference/method/db.collection.updateMany/
// nota: la API OBLIGA a elegir: updateOne o updateMany, deleteOne o deleteMany.
//       Ese nombre explicito es mejor defensa que la de SQL, donde una sola
//       palabra separa una fila de un millon. Lo que no cambia: deleteMany({})
//       vacia la coleccion, y el filtro vacio es lo que devuelve un objeto sin
//       inicializar.

// === preparacion ===
db.notas.drop();
db.notas.insertMany([
  { estudiante: "Ada", curso: "DB-101", nota: 90 },
  { estudiante: "Linus", curso: "DB-101", nota: 58 },
  { estudiante: "Grace", curso: "DB-101", nota: 72 },
  { estudiante: "Ada", curso: "SE-201", nota: 66 },
]);

const subidas = db.notas.updateMany({ curso: "DB-101" }, { $inc: { nota: 5 } });
const bajas = db.notas.deleteMany({ estudiante: "Linus" });
if (subidas.modifiedCount !== 3 || bajas.deletedCount !== 1) {
  throw new Error("el alcance del cambio no era el esperado");
}

// === consulta ===
db.notas
  .find({}, { _id: 0 })
  .sort({ estudiante: 1, curso: 1 })
  .forEach((d) => print(d.estudiante + "|" + d.curso + "|" + d.nota));
