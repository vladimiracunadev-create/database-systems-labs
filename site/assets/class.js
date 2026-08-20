// Pagina de clase: avance de lectura, marca de completada y copiar codigo.

(() => {
  const barra = document.querySelector(".avance");
  if (barra) {
    const pintar = () => {
      const alto = document.documentElement.scrollHeight - window.innerHeight;
      const razon = alto > 0 ? window.scrollY / alto : 1;
      barra.style.width = `${Math.min(100, Math.max(0, razon * 100))}%`;
    };
    document.addEventListener("scroll", pintar, { passive: true });
    window.addEventListener("resize", pintar);
    pintar();
  }

  const boton = document.getElementById("completar");
  if (boton) {
    const id = boton.dataset.clase;
    const pintar = () => {
      const hecho = window.DSL.completadas().has(id);
      boton.setAttribute("aria-pressed", String(hecho));
      boton.textContent = hecho ? "✓ Clase completada" : "Marcar como completada";
    };
    boton.addEventListener("click", () => {
      window.DSL.marcar(id, boton.getAttribute("aria-pressed") !== "true");
      pintar();
    });
    pintar();
  }

  // Copiar el contenido de cada bloque de codigo. Sin el portapapeles del
  // navegador (contexto no seguro, permiso denegado) el boton no aparece.
  if (navigator.clipboard) {
    for (const bloque of document.querySelectorAll("main pre")) {
      if (bloque.classList.contains("mermaid")) continue;
      const copiar = document.createElement("button");
      copiar.className = "copiar";
      copiar.type = "button";
      copiar.textContent = "copiar";
      copiar.addEventListener("click", async () => {
        try {
          await navigator.clipboard.writeText(bloque.innerText.replace(/\ncopiar$/, ""));
          copiar.textContent = "copiado";
        } catch {
          copiar.textContent = "no se pudo";
        }
        setTimeout(() => { copiar.textContent = "copiar"; }, 1600);
      });
      bloque.appendChild(copiar);
    }
  }
})();
