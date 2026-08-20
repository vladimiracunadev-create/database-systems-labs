// motor: mongodb
// doc: https://www.mongodb.com/docs/manual/faq/fundamentals/
// nota: la inyeccion clasica no existe —las consultas son documentos, no
//       cadenas— pero hay otra. Si `entrada` viene de un cuerpo JSON sin
//       comprobar el tipo y resulta ser un OBJETO:
//         entrada = { "$ne": null }
//         db.usuarios.find({ nombre: entrada })   -> devuelve TODOS
//       Eso es inyeccion de OPERADOR, y la defensa no es escapar: es comprobar
//       que lo recibido es una cadena antes de construir el filtro.

// === preparacion ===
db.usuarios.drop();
db.usuarios.insertMany([
  { nombre: "ada", rol: "admin" },
  { nombre: "linus", rol: "lector" },
  { nombre: "grace", rol: "lector" },
]);

// === consulta ===
const entrada = "' OR '1'='1";
if (typeof entrada !== "string") throw new Error("entrada no es una cadena");
print(db.usuarios.countDocuments({ nombre: entrada }));
