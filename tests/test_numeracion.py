"""Que el número que se lee coincida con el destino al que lleva.

Este archivo nace de un fallo real. Al insertar la parte 00 se renumeraron las
74 clases, y los scripts actualizaron **las rutas** de todos los enlaces. Lo que
no actualizó nadie fue el **texto** de esos enlaces: quedaron 55 etiquetas
diciendo «017 — Agregación» sobre un enlace que llevaba a `027-agregacion…`, y
18 más diciendo «Parte 13» sobre `part-14-…`.

Es el peor tipo de error de documentación: los enlaces funcionan, la validación
pasa, la navegación no se rompe, y aun así el material miente al lector en cada
referencia cruzada. Solo se ve leyendo, y por eso hace falta una prueba.

La regla es que el destino manda: la carpeta existe y el validador ya comprueba
que el enlace resuelve, así que si etiqueta y destino discrepan, la equivocada
es siempre la etiqueta.
"""

from __future__ import annotations

import re
from pathlib import Path

import pytest
import yaml

RAIZ = Path(__file__).resolve().parents[1]
IGNORAR = {"node_modules", ".git", "site", ".venv", "__pycache__"}

# [017 — Agregación…](../classes/part-04-…/027-agregacion…/README.md)
ETIQUETA_CLASE = re.compile(
    r"\[(\d{3})\s*—\s*([^\]]+)\]\([^)]*?(\d{3})-[a-z0-9-]+/README\.md\)")
# [Parte 13 — Vectores…](../classes/part-14-…/README.md)
ETIQUETA_PARTE = re.compile(
    r"\[(?:Parte\s+)?(\d{2})\s*—\s*([^\]]+)\]\([^)]*?part-(\d{2})-[a-z0-9-]+/README\.md\)")


def documentos() -> list[Path]:
    return [p for p in sorted(RAIZ.rglob("*.md"))
            if not IGNORAR & set(p.relative_to(RAIZ).parts)]


@pytest.fixture(scope="module")
def curriculo() -> dict:
    return yaml.safe_load((RAIZ / "curriculum.yaml").read_text(encoding="utf-8"))


def test_la_etiqueta_de_una_clase_coincide_con_la_clase_enlazada() -> None:
    desajustes = []
    for documento in documentos():
        texto = documento.read_text(encoding="utf-8")
        for etiqueta, titulo, destino in ETIQUETA_CLASE.findall(texto):
            if etiqueta != destino:
                desajustes.append(
                    f"{documento.relative_to(RAIZ)}: dice «{etiqueta} — "
                    f"{titulo.strip()[:40]}» pero enlaza a la clase {destino}")
    assert not desajustes, "etiquetas de clase desincronizadas:\n  " + "\n  ".join(desajustes)


def test_la_etiqueta_de_una_parte_coincide_con_la_parte_enlazada() -> None:
    desajustes = []
    for documento in documentos():
        if "classes" in documento.relative_to(RAIZ).parts:
            continue  # los índices generados numeran desde el currículo
        texto = documento.read_text(encoding="utf-8")
        for etiqueta, titulo, destino in ETIQUETA_PARTE.findall(texto):
            if etiqueta != destino:
                desajustes.append(
                    f"{documento.relative_to(RAIZ)}: dice «{etiqueta} — "
                    f"{titulo.strip()[:40]}» pero enlaza a la parte {destino}")
    assert not desajustes, "etiquetas de parte desincronizadas:\n  " + "\n  ".join(desajustes)


def test_cada_guia_de_ruta_recorre_las_partes_que_declara(curriculo: dict) -> None:
    """La guía que lee una persona y la ruta del currículo tienen que coincidir.

    Cuando se añadió la parte 00, el currículo la incorporó a las siete rutas y
    la insignia —generada— lo reflejó al instante. El cuerpo de las guías, que
    se escribe a mano, se quedó una parte corto en las siete.
    """
    faltantes = []
    for slug, ruta in curriculo["rutas"].items():
        texto = (RAIZ / "rutas" / f"{slug}.md").read_text(encoding="utf-8")
        for pid in ruta["partes"]:
            if f"part-{pid}-" not in texto:
                faltantes.append(f"{slug}.md no menciona la parte {pid}")
    assert not faltantes, "guías de ruta incompletas:\n  " + "\n  ".join(faltantes)


def test_la_prosa_de_cada_ruta_declara_las_partes_y_horas_reales(curriculo: dict) -> None:
    horas = {p["id"]: sum(c["hours"] for c in p["classes"]) for p in curriculo["parts"]}
    errores = []
    for slug, ruta in curriculo["rutas"].items():
        texto = (RAIZ / "rutas" / f"{slug}.md").read_text(encoding="utf-8")
        esperado = (len(ruta["partes"]), sum(horas[p] for p in ruta["partes"]))
        prosa = re.search(r"(?:^|\n)(?:Las )?(\d+) partes, (\d+) horas", texto)
        assert prosa, f"{slug}.md no declara cuántas partes y horas tiene la ruta"
        if (int(prosa.group(1)), int(prosa.group(2))) != esperado:
            errores.append(
                f"{slug}.md dice {prosa.group(1)} partes y {prosa.group(2)} h; "
                f"el currículo suma {esperado[0]} y {esperado[1]}")
    assert not errores, "conteos de ruta desincronizados:\n  " + "\n  ".join(errores)


def test_ningun_documento_actual_afirma_las_cifras_del_programa_anterior() -> None:
    """La prueba de fuego: las cifras de la versión 2.0 solo pueden vivir en la historia.

    64 clases, 14 partes y 210 horas fueron ciertas hasta que la parte 00 entró
    en el programa. Siguen siendo legítimas dentro del CHANGELOG y del ROADMAP,
    que narran lo que pasó; en cualquier otro sitio son una mentira.
    """
    historicos = {"CHANGELOG.md", "ROADMAP.md"}
    viejas = ("64 clases", "210 horas", "14 partes")
    encontradas = []
    for documento in documentos():
        if documento.name in historicos:
            continue
        texto = documento.read_text(encoding="utf-8")
        for cifra in viejas:
            if cifra in texto:
                encontradas.append(f"{documento.relative_to(RAIZ)}: «{cifra}»")
    assert not encontradas, (
        "cifras del programa anterior presentadas como actuales:\n  "
        + "\n  ".join(encontradas))
