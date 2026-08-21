// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/core/views/
// nota: la vista de solo lectura con la tuberia filtrada, mas un rol que de
//       acceso a la vista y NO a la coleccion, consigue la misma frontera:
//         db.createRole({ role: "acme_lector",
//                         privileges: [{ resource: { db: "learning",
//                                                    collection: "mis_notas" },
//                                        actions: ["find"] }], roles: [] })
//       En la version Community no hay control por documento: es por coleccion.

// === preparacion ===
db.mis_notas.drop();
db.notas.drop();

db.notas.insertMany([
  { inquilino: "acme", estudiante: "Ada", nota: 90 },
  { inquilino: "acme", estudiante: "Bea", nota: 58 },
  { inquilino: "globex", estudiante: "Cid", nota: 77 },
]);

db.createView("mis_notas", "notas", [
  { $match: { inquilino: "acme" } },
  { $project: { _id: 0, estudiante: 1, nota: 1 } },
]);

// === consulta ===
db.mis_notas
  .find()
  .sort({ estudiante: 1 })
  .forEach((d) => print(d.estudiante + "|" + d.nota));
