// Portada: filtrado del catalogo y progreso, en el cliente y sin dependencias.
//
// El indice viene en `busqueda.json` en vez de leerse del DOM: asi la busqueda
// alcanza tambien los conceptos y las fuentes de cada clase, que no se pintan
// enteros en la tarjeta.

(async () => {
  const $ = (sel) => document.querySelector(sel);
  const entrada = $("#q");
  const selParte = $("#parte");
  const selNivel = $("#nivel");
  const selMotor = $("#motor");
  const soloPendientes = $("#pendientes");
  const contador = $("#contador");
  if (!entrada) return;

  let indice = [];
  try {
    indice = await (await fetch("busqueda.json")).json();
  } catch {
    // Sin indice, los filtros de texto se desactivan pero las tarjetas siguen
    // visibles: es preferible a una pagina en blanco.
    entrada.disabled = true;
    entrada.placeholder = "Índice de búsqueda no disponible";
  }
  const porId = new Map(indice.map((c) => [c.id, c]));

  const normaliza = (s) =>
    s.toLowerCase().normalize("NFD").replace(/[̀-ͯ]/g, "");

  const tarjetas = [...document.querySelectorAll("[data-clase]")];

  function pintarProgreso() {
    const hechas = window.DSL.completadas();
    for (const el of tarjetas) {
      el.classList.toggle("completada", hechas.has(el.dataset.clase));
    }
    const marcador = $("#progreso");
    if (marcador) marcador.textContent = `${hechas.size}/${tarjetas.length}`;
    const barra = $("#progreso-barra");
    if (barra) {
      const porcentaje = Math.round((hechas.size / tarjetas.length) * 100);
      barra.style.width = `${porcentaje}%`;
      barra.parentElement.setAttribute("aria-valuenow", String(porcentaje));
    }
    return hechas;
  }

  function aplicar() {
    const hechas = pintarProgreso();
    const q = normaliza(entrada.value.trim());
    const parte = selParte.value;
    const nivel = selNivel.value;
    const motor = selMotor.value;
    const pendientes = soloPendientes && soloPendientes.checked;
    let visibles = 0;

    for (const el of tarjetas) {
      const id = el.dataset.clase;
      const c = porId.get(id);
      const texto = c ? c.buscable : normaliza(el.textContent);
      const ok =
        (!q || texto.includes(q)) &&
        (!parte || el.dataset.parte === parte) &&
        (!nivel || el.dataset.nivel === nivel) &&
        (!motor || (el.dataset.motores || "").split(",").includes(motor)) &&
        (!pendientes || !hechas.has(id));
      el.classList.toggle("hidden", !ok);
      if (ok) visibles++;
    }

    // Una parte sin clases visibles se oculta entera: evita cabeceras huerfanas.
    for (const bloque of document.querySelectorAll(".part")) {
      const alguna = bloque.querySelector("[data-clase]:not(.hidden)");
      bloque.classList.toggle("hidden", !alguna);
    }

    contador.textContent =
      visibles === tarjetas.length
        ? `${tarjetas.length} clases`
        : `${visibles} de ${tarjetas.length} clases`;
    $("#vacio").classList.toggle("hidden", visibles > 0);
  }

  for (const control of [entrada, selParte, selNivel, selMotor, soloPendientes]) {
    if (control) control.addEventListener("input", aplicar);
  }

  // "/" enfoca la busqueda, salvo que ya se este escribiendo en otro campo.
  document.addEventListener("keydown", (e) => {
    if (e.key === "/" && !/^(INPUT|SELECT|TEXTAREA)$/.test(document.activeElement.tagName)) {
      e.preventDefault();
      entrada.focus();
    }
    if (e.key === "Escape" && document.activeElement === entrada) {
      entrada.value = "";
      aplicar();
    }
  });

  // El progreso puede cambiar en otra pestana: se refleja sin recargar.
  window.addEventListener("storage", aplicar);
  window.addEventListener("pageshow", aplicar);

  aplicar();
})();
