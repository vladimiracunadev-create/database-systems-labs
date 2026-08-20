// Cache del sitio para consulta sin conexion.
// La version sale de la huella del contenido generado: si cambia una pagina,
// cambia el nombre de la cache y la anterior se descarta entera.
const CACHE = "database-systems-labs-1286d9a211ca";
const ESENCIALES = ["./", "./index.html", "./laboratorios.html", "./autoevaluacion.html", "./fuentes.html", "./motores.html", "./busqueda.json", "./assets/styles.css", "./assets/class.css", "./assets/comun.js", "./assets/app.js", "./assets/class.js", "./assets/icon.svg"];

self.addEventListener("install", (evento) => {
  self.skipWaiting();
  evento.waitUntil(caches.open(CACHE).then((cache) => cache.addAll(ESENCIALES)));
});

self.addEventListener("activate", (evento) => {
  evento.waitUntil(caches.keys().then((claves) => Promise.all(
    claves.filter((clave) => clave !== CACHE).map((clave) => caches.delete(clave)),
  )).then(() => self.clients.claim()));
});

// Red primero: el material cambia y una copia vieja confunde mas de lo que
// ayuda. La cache solo responde cuando no hay conexion.
self.addEventListener("fetch", (evento) => {
  if (evento.request.method !== "GET") return;
  evento.respondWith(fetch(evento.request).then((respuesta) => {
    const copia = respuesta.clone();
    caches.open(CACHE).then((cache) => cache.put(evento.request, copia));
    return respuesta;
  }).catch(() => caches.match(evento.request).then(
    (guardada) => guardada || caches.match("./index.html"),
  )));
});
