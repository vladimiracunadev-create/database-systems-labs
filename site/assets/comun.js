// Utilidades compartidas por todas las paginas: tema y progreso.
//
// Todo vive en el navegador de quien estudia: no hay servidor, ni cuenta, ni
// analitica. Si alguien borra el almacenamiento local, pierde su progreso y no
// pasa nada mas.

window.DSL = (() => {
  const CLAVE_TEMA = "dsl:tema";
  const CLAVE_PROGRESO = "dsl:completadas";

  const almacen = (() => {
    try {
      // En navegacion privada de algunos navegadores `localStorage` existe pero
      // lanza al escribir: se comprueba una vez y se degrada a memoria.
      const prueba = "dsl:prueba";
      window.localStorage.setItem(prueba, "1");
      window.localStorage.removeItem(prueba);
      return window.localStorage;
    } catch {
      const memoria = new Map();
      return {
        getItem: (k) => (memoria.has(k) ? memoria.get(k) : null),
        setItem: (k, v) => memoria.set(k, v),
        removeItem: (k) => memoria.delete(k),
      };
    }
  })();

  function temaGuardado() {
    return almacen.getItem(CLAVE_TEMA);
  }

  function aplicarTema(tema) {
    if (tema) {
      document.documentElement.dataset.tema = tema;
      almacen.setItem(CLAVE_TEMA, tema);
    } else {
      delete document.documentElement.dataset.tema;
      almacen.removeItem(CLAVE_TEMA);
    }
    const oscuro =
      document.documentElement.dataset.tema === "oscuro" ||
      (!document.documentElement.dataset.tema &&
        !window.matchMedia("(prefers-color-scheme: light)").matches);
    const boton = document.getElementById("tema");
    if (boton) {
      boton.textContent = oscuro ? "☾" : "☀";
      boton.setAttribute(
        "title",
        oscuro ? "Cambiar a tema claro" : "Cambiar a tema oscuro",
      );
    }
    const meta = document.querySelector('meta[name="theme-color"]');
    if (meta) meta.content = oscuro ? "#05090f" : "#f7fafd";
  }

  function conmutarTema() {
    const actual = document.documentElement.dataset.tema;
    const oscuroAhora =
      actual === "oscuro" ||
      (!actual && !window.matchMedia("(prefers-color-scheme: light)").matches);
    aplicarTema(oscuroAhora ? "claro" : "oscuro");
  }

  function completadas() {
    try {
      const crudo = JSON.parse(almacen.getItem(CLAVE_PROGRESO) || "[]");
      return new Set(Array.isArray(crudo) ? crudo : []);
    } catch {
      return new Set();
    }
  }

  function marcar(id, hecho) {
    const conjunto = completadas();
    if (hecho) conjunto.add(id);
    else conjunto.delete(id);
    almacen.setItem(CLAVE_PROGRESO, JSON.stringify([...conjunto].sort()));
    return conjunto;
  }

  document.addEventListener("DOMContentLoaded", () => {
    aplicarTema(temaGuardado());
    const boton = document.getElementById("tema");
    if (boton) boton.addEventListener("click", conmutarTema);
  });

  return { completadas, marcar, aplicarTema, conmutarTema };
})();
