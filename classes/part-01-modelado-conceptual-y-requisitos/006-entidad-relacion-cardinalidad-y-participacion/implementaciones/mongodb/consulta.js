// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/data-modeling/
// nota: aqui la relacion vive como un arreglo de referencias dentro del curso.
//       Es el modelo natural cuando la pregunta frecuente es «quienes estan en
//       este curso»; la pregunta inversa exige un indice multiclave.

// === preparacion ===
db.cursos.drop();
db.estudiantes.drop();

db.estudiantes.insertMany([
  { _id: 1, nombre: "Ada" },
  { _id: 2, nombre: "Linus" },
  { _id: 3, nombre: "Grace" },
]);
db.cursos.insertMany([
  { _id: 10, codigo: "DB-101", inscritos: [1, 2] },
  { _id: 20, codigo: "SE-201", inscritos: [1] },
  // Participacion parcial: el curso existe con el arreglo vacio.
  { _id: 30, codigo: "AR-301", inscritos: [] },
]);

// === consulta ===
db.cursos
  .aggregate([
    { $project: { _id: 0, curso: "$codigo", estudiantes: { $size: "$inscritos" } } },
    { $sort: { curso: 1 } },
  ])
  .forEach((d) => print(d.curso + "|" + d.estudiantes));
