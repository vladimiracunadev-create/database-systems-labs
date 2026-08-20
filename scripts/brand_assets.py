"""Marca grafica del programa, generada sin dependencias.

Produce el icono de la aplicacion (192 y 512 px) y la portada social
(1200x630) que usan las etiquetas Open Graph. Los tres son artefactos
derivados: se regeneran en cada ejecucion y `--check` falla si el archivo del
repositorio no coincide, igual que con el resto del sitio.

Se escriben con `zlib` y `struct` de la biblioteca estandar, sin Pillow ni
ninguna otra dependencia, por la misma razon por la que los laboratorios del
nucleo no la tienen: un artefacto que solo se puede regenerar en la maquina de
quien lo creo no es reproducible.

Formato PNG: RGB de 8 bits, sin entrelazado, filtro 0 por fila.
Referencia normativa: W3C, "Portable Network Graphics (PNG) Specification
(Third Edition)", https://www.w3.org/TR/png-3/

El dibujo es un cilindro de datos —la convencion visual de una base de datos
desde los diagramas de flujo de ISO 5807— sobre un fondo con los mismos colores
que el sitio.
"""

from __future__ import annotations

import struct
import zlib

# Paleta compartida con site/assets/styles.css. Si cambia alli, cambia aqui.
FONDO = (0x05, 0x09, 0x0F)
PANEL = (0x0D, 0x16, 0x22)
TEAL = (0x2E, 0xE6, 0xC5)
AZURE = (0x4A, 0xA8, 0xFF)
AMBER = (0xFF, 0xC8, 0x61)


# --------------------------------------------------------------------------- #
# Codificacion PNG
# --------------------------------------------------------------------------- #

def _chunk(tipo: bytes, datos: bytes) -> bytes:
    return (struct.pack(">I", len(datos)) + tipo + datos
            + struct.pack(">I", zlib.crc32(tipo + datos) & 0xFFFFFFFF))


def png(ancho: int, alto: int, pixeles: bytearray) -> bytes:
    """Codifica un buffer RGB (3 bytes por pixel, sin relleno) como PNG."""
    if len(pixeles) != ancho * alto * 3:
        raise ValueError("el buffer no corresponde al tamano declarado")
    filas = bytearray()
    paso = ancho * 3
    for y in range(alto):
        filas.append(0)  # filtro "None": el contenido ya es plano y comprime bien
        filas += pixeles[y * paso:(y + 1) * paso]
    return (b"\x89PNG\r\n\x1a\n"
            + _chunk(b"IHDR", struct.pack(">IIBBBBB", ancho, alto, 8, 2, 0, 0, 0))
            + _chunk(b"IDAT", zlib.compress(bytes(filas), 9))
            + _chunk(b"IEND", b""))


# --------------------------------------------------------------------------- #
# Dibujo
# --------------------------------------------------------------------------- #

def _mezcla(fondo: tuple, frente: tuple, alfa: float) -> tuple:
    return tuple(f + (d - f) * alfa for f, d in zip(fondo, frente))


def _degradado(a: tuple, b: tuple, t: float) -> tuple:
    t = 0.0 if t < 0 else 1.0 if t > 1 else t
    return tuple(x + (y - x) * t for x, y in zip(a, b))


def _cobertura_elipse(x: float, y: float, cx: float, cy: float,
                      rx: float, ry: float, suavizado: float) -> float:
    """Cobertura antialias de una elipse, por distancia normalizada al borde."""
    dx = (x - cx) / rx
    dy = (y - cy) / ry
    distancia = (dx * dx + dy * dy) ** 0.5
    borde = suavizado / min(rx, ry)
    if distancia <= 1 - borde:
        return 1.0
    if distancia >= 1 + borde:
        return 0.0
    return (1 + borde - distancia) / (2 * borde)


def _cobertura_rect_redondeado(x: float, y: float, x0: float, y0: float,
                               x1: float, y1: float, radio: float,
                               suavizado: float = 1.0) -> float:
    """Cobertura antialias de un rectangulo de esquinas redondeadas."""
    cx = min(max(x, x0 + radio), x1 - radio)
    cy = min(max(y, y0 + radio), y1 - radio)
    distancia = (((x - cx) ** 2 + (y - cy) ** 2) ** 0.5) - radio
    if distancia <= -suavizado:
        return 1.0
    if distancia >= suavizado:
        return 0.0
    return (suavizado - distancia) / (2 * suavizado)


def _cilindro(x: float, y: float, cx: float, cy: float,
              ancho: float, alto: float) -> tuple[float, float]:
    """Devuelve (cobertura, t) del cilindro de datos; `t` sirve para el degradado.

    El cilindro son tres discos apilados: la union de la tapa, el cuerpo y la
    base. Se evalua analiticamente para que el borde salga suave a cualquier
    tamano, sin muestreo multiple.
    """
    rx = ancho / 2
    ry = ancho / 7          # aplastamiento de las tapas
    cuerpo = alto / 2 - ry  # media altura del tramo recto
    suavizado = max(ancho / 220, 0.6)

    cobertura = 0.0
    # Tapa y base.
    for centro in (cy - cuerpo, cy + cuerpo):
        cobertura = max(cobertura, _cobertura_elipse(x, y, cx, centro, rx, ry, suavizado))
    # Cuerpo recto, con los lados suavizados como el resto.
    if cy - cuerpo <= y <= cy + cuerpo:
        lateral = abs(x - cx) - rx
        if lateral <= -suavizado:
            cobertura = 1.0
        elif lateral < suavizado:
            cobertura = max(cobertura, (suavizado - lateral) / (2 * suavizado))

    t = (y - (cy - alto / 2)) / alto
    return cobertura, t


def _bandas(x: float, y: float, cx: float, cy: float,
            ancho: float, alto: float) -> float:
    """Las dos lineas que separan los discos del cilindro."""
    rx = ancho / 2
    ry = ancho / 7
    cuerpo = alto / 2 - ry
    grosor = max(ancho / 40, 1.0)
    cobertura = 0.0
    for centro in (cy - cuerpo / 3, cy + cuerpo / 3):
        fuera = _cobertura_elipse(x, y, cx, centro, rx, ry, 0.8)
        dentro = _cobertura_elipse(x, y, cx, centro, rx - grosor, ry - grosor * 0.35, 0.8)
        # Solo la mitad inferior de cada elipse: es la que se ve en un cilindro.
        if y >= centro:
            cobertura = max(cobertura, fuera - dentro)
    return max(cobertura, 0.0)


def icono(lado: int) -> bytes:
    """Icono cuadrado: cilindro de datos sobre un panel redondeado."""
    pixeles = bytearray(lado * lado * 3)
    margen = lado * 0.06
    radio = lado * 0.22
    cx = cy = lado / 2
    ancho_cil = lado * 0.52
    alto_cil = lado * 0.60
    suavizado = max(lado / 256, 0.7)

    # Fuera de estas franjas el pixel es fondo puro o panel puro, y no hace
    # falta evaluar la geometria: el dibujo cuesta la mitad de tiempo.
    x_borde_izq = margen + radio + 2
    x_borde_der = lado - margen - radio - 2
    cil_x0, cil_x1 = cx - ancho_cil / 2 - 2, cx + ancho_cil / 2 + 2
    cil_y0, cil_y1 = cy - alto_cil / 2 - 2, cy + alto_cil / 2 + 2

    i = 0
    for py in range(lado):
        y = py + 0.5
        # El panel es un degradado vertical: su color solo depende de la fila.
        panel_color = _degradado(PANEL, (0x14, 0x2A, 0x3E), y / lado)
        fila_interior = margen + radio <= y <= lado - margen - radio
        fila_fuera = y < margen - 1 or y > lado - margen + 1
        fila_cilindro = cil_y0 <= y <= cil_y1

        for px in range(lado):
            x = px + 0.5
            if fila_fuera:
                color = FONDO
            elif fila_interior and x_borde_izq <= x <= x_borde_der:
                color = panel_color  # bien dentro del panel: sin borde que suavizar
            else:
                panel = _cobertura_rect_redondeado(x, y, margen, margen,
                                                   lado - margen, lado - margen,
                                                   radio, suavizado)
                color = _mezcla(FONDO, panel_color, panel)

            if fila_cilindro and cil_x0 <= x <= cil_x1:
                cobertura, t = _cilindro(x, y, cx, cy, ancho_cil, alto_cil)
                if cobertura > 0:
                    color = _mezcla(color, _degradado(TEAL, AZURE, t), cobertura)
                    banda = _bandas(x, y, cx, cy, ancho_cil, alto_cil)
                    if banda > 0:
                        color = _mezcla(color, FONDO, banda * 0.55)

            pixeles[i] = int(color[0] + 0.5)
            pixeles[i + 1] = int(color[1] + 0.5)
            pixeles[i + 2] = int(color[2] + 0.5)
            i += 3
    return png(lado, lado, pixeles)


def portada(ancho: int = 1200, alto: int = 630) -> bytes:
    """Portada social: la marca y una barra por cada parte del programa."""
    from math import exp

    pixeles = bytearray(ancho * alto * 3)
    cx, cy = ancho * 0.22, alto * 0.47
    ancho_cil = alto * 0.34
    alto_cil = alto * 0.40

    # Alturas de las 14 barras: proporcionales a las clases de cada parte
    # (4, 5, 4, 6, 4, 4, 5, 5, 5, 5, 6, 4, 4, 3), normalizadas.
    clases_por_parte = [4, 5, 4, 6, 4, 4, 5, 5, 5, 5, 6, 4, 4, 3]
    maximo = max(clases_por_parte)
    # El ancho de barra sale del espacio disponible, no de una constante: asi la
    # serie termina siempre dentro del lienzo aunque cambie el numero de partes.
    x0_barras = ancho * 0.44
    x1_barras = ancho * 0.92
    paso = (x1_barras - x0_barras) / len(clases_por_parte)
    barra_ancho = paso * 0.68
    base = alto * 0.72

    # El fondo son dos focos de luz: exp() se consulta en una tabla en vez de
    # calcularse un millon de veces, y la raiz cuadrada se evita usando el
    # cuadrado de la distancia, que es lo unico que necesita la exponencial.
    PASOS_LUT = 4096
    TOPE = 20.0
    lut = [exp(-i * TOPE / PASOS_LUT) for i in range(PASOS_LUT)]
    norma1 = (alto * 0.9) ** 2
    norma2 = (alto * 0.8) ** 2
    foco1_x, foco1_y = ancho * 0.85, -alto * 0.15
    foco2_x, foco2_y = ancho * 0.05, alto * 0.05
    dx1 = [(px + 0.5 - foco1_x) ** 2 for px in range(ancho)]
    dx2 = [(px + 0.5 - foco2_x) ** 2 for px in range(ancho)]

    cil_x0, cil_x1 = cx - ancho_cil / 2 - 2, cx + ancho_cil / 2 + 2
    cil_y0, cil_y1 = cy - alto_cil / 2 - 2, cy + alto_cil / 2 + 2
    tope_barras = base - alto * 0.30 - 2

    i = 0
    for py in range(alto):
        y = py + 0.5
        dy1 = (y - foco1_y) ** 2
        dy2 = (y - foco2_y) ** 2
        fila_cilindro = cil_y0 <= y <= cil_y1
        fila_barras = tope_barras <= y <= base + 3

        for px in range(ancho):
            q1 = (dx1[px] + dy1) / norma1 * PASOS_LUT / TOPE
            q2 = (dx2[px] + dy2) / norma2 * PASOS_LUT / TOPE
            f1 = lut[int(q1)] * 0.85 if q1 < PASOS_LUT else 0.0
            f2 = lut[int(q2)] * 0.70 if q2 < PASOS_LUT else 0.0
            r = FONDO[0] + (0x13 - FONDO[0]) * f1
            g = FONDO[1] + (0x32 - FONDO[1]) * f1
            b = FONDO[2] + (0x4A - FONDO[2]) * f1
            r += (0x0F - r) * f2
            g += (0x2C - g) * f2
            b += (0x3A - b) * f2
            color = (r, g, b)

            x = px + 0.5
            if fila_cilindro and cil_x0 <= x <= cil_x1:
                cobertura, t = _cilindro(x, y, cx, cy, ancho_cil, alto_cil)
                if cobertura > 0:
                    color = _mezcla(color, _degradado(TEAL, AZURE, t), cobertura)
                    banda = _bandas(x, y, cx, cy, ancho_cil, alto_cil)
                    if banda > 0:
                        color = _mezcla(color, FONDO, banda * 0.55)

            # Barras: una por parte, altura proporcional a sus clases.
            elif fila_barras and x0_barras <= x <= x1_barras:
                indice = int((x - x0_barras) // paso)
                if 0 <= indice < len(clases_por_parte):
                    inicio_barra = x0_barras + indice * paso
                    if inicio_barra <= x <= inicio_barra + barra_ancho:
                        altura = alto * 0.30 * clases_por_parte[indice] / maximo
                        cobertura_barra = _cobertura_rect_redondeado(
                            x, y, inicio_barra, base - altura,
                            inicio_barra + barra_ancho, base, barra_ancho / 2, 0.8)
                        if cobertura_barra > 0:
                            tinta = _degradado(AZURE, AMBER,
                                               indice / (len(clases_por_parte) - 1))
                            color = _mezcla(color, tinta, cobertura_barra * 0.92)
                # Linea base bajo las barras.
                if base <= y <= base + 2:
                    color = (0x1D, 0x2F, 0x45)

            pixeles[i] = int(color[0] + 0.5)
            pixeles[i + 1] = int(color[1] + 0.5)
            pixeles[i + 2] = int(color[2] + 0.5)
            i += 3
    return png(ancho, alto, pixeles)


def generar() -> dict[str, bytes]:
    """Los tres artefactos de marca, listos para escribirse en site/assets."""
    return {
        "icon-192.png": icono(192),
        "icon-512.png": icono(512),
        "og-cover.png": portada(),
    }


if __name__ == "__main__":
    from pathlib import Path

    destino = Path(__file__).resolve().parents[1] / "site" / "assets"
    for nombre, contenido in generar().items():
        (destino / nombre).write_bytes(contenido)
        print(f"{nombre}: {len(contenido):,} bytes")
