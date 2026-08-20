"""Laboratorio 07 - Replica, retraso y garantias de sesion.

Un lider y dos seguidores con retraso de replica declarado. El laboratorio
cuenta cuantas lecturas devuelven datos viejos y cuantas rompen garantias que
la aplicacion daba por hechas, y despues aplica las tres correcciones que
existen: leer del lider, esperar a la posicion escrita (garantia de sesion) o
exigir quorum.

Nada de esto se mide con un cronometro: el reloj es logico y el retraso se
declara en ticks. Un tiempo dependeria de la maquina; el numero de lecturas
obsoletas depende solo del modelo, y por eso es evidencia comparable.

Sin dependencias externas: solo la biblioteca estandar.

Uso:
    python labs/07-replication/run_replication_lab.py
"""

from __future__ import annotations

from dataclasses import dataclass, field

RETRASOS = {"seguidor-a": 2, "seguidor-b": 5}  # ticks que tarda en aplicar cada escritura
CLIENTES = 6                                   # escrituras del cliente que luego relee


@dataclass
class Escritura:
    """Una escritura confirmada por el lider, con su posicion en el registro."""

    lsn: int      # numero de secuencia del registro (log sequence number)
    clave: str
    valor: str
    tick: int     # momento logico en que el lider la confirmo


@dataclass
class Replica:
    """Un seguidor que aplica el registro del lider con un retraso fijo."""

    nombre: str
    retraso: int
    aplicadas: list[Escritura] = field(default_factory=list)

    def aplicar_hasta(self, registro: list[Escritura], ahora: int) -> None:
        # Solo llega lo que el lider confirmo hace al menos `retraso` ticks.
        self.aplicadas = [e for e in registro if e.tick + self.retraso <= ahora]

    def leer(self, clave: str) -> tuple[str | None, int]:
        """Devuelve (valor, lsn) de la version que este seguidor conoce."""
        vistas = [e for e in self.aplicadas if e.clave == clave]
        if not vistas:
            return None, 0
        ultima = vistas[-1]
        return ultima.valor, ultima.lsn

    @property
    def posicion(self) -> int:
        return self.aplicadas[-1].lsn if self.aplicadas else 0


class Cluster:
    """Un lider, dos seguidores y un reloj logico compartido."""

    def __init__(self) -> None:
        self.tick = 0
        self.registro: list[Escritura] = []
        self.replicas = [Replica(nombre, retraso) for nombre, retraso in RETRASOS.items()]

    def avanzar(self, ticks: int = 1) -> None:
        self.tick += ticks
        for replica in self.replicas:
            replica.aplicar_hasta(self.registro, self.tick)

    def escribir(self, clave: str, valor: str) -> int:
        """Escritura confirmada por el lider; devuelve la posicion del registro."""
        lsn = len(self.registro) + 1
        self.registro.append(Escritura(lsn, clave, valor, self.tick))
        return lsn

    def leer_del_lider(self, clave: str) -> tuple[str | None, int]:
        vistas = [e for e in self.registro if e.clave == clave]
        if not vistas:
            return None, 0
        return vistas[-1].valor, vistas[-1].lsn

    @property
    def retraso_maximo(self) -> int:
        """Ticks que separan al seguidor mas lento del lider."""
        return max(self.tick - (r.aplicadas[-1].tick if r.aplicadas else 0)
                   for r in self.replicas) if self.registro else 0


# --------------------------------------------------------------------------- #
# Cuatro estrategias de lectura sobre el mismo escenario.
# El cliente escribe su perfil y lo relee inmediatamente, como haria cualquier
# aplicacion despues de un formulario.
# --------------------------------------------------------------------------- #

def escenario(estrategia: str) -> dict[str, int]:
    cluster = Cluster()
    violaciones_lectura_propia = 0
    lecturas_obsoletas = 0
    lecturas_no_monotonas = 0
    esperas = 0
    ultimo_lsn_visto = 0

    for i in range(CLIENTES):
        valor = f"perfil-v{i + 1}"
        lsn = cluster.escribir("usuario:42", valor)
        cluster.avanzar(1)  # el cliente relee casi enseguida

        if estrategia == "lider":
            leido, lsn_leido = cluster.leer_del_lider("usuario:42")
        elif estrategia == "seguidor":
            # Reparto entre seguidores, como haria un balanceador cualquiera.
            leido, lsn_leido = cluster.replicas[i % len(cluster.replicas)].leer("usuario:42")
        elif estrategia == "sesion":
            # Garantia de sesion: se espera a que el seguidor alcance la
            # posicion que este cliente acaba de escribir.
            replica = cluster.replicas[i % len(cluster.replicas)]
            while replica.posicion < lsn:
                cluster.avanzar(1)
                esperas += 1
            leido, lsn_leido = replica.leer("usuario:42")
        elif estrategia == "quorum":
            # R + W > N: se leen dos replicas de tres nodos (lider incluido) y
            # se resuelve por la version mas alta.
            respuestas = [cluster.leer_del_lider("usuario:42"),
                          cluster.replicas[i % len(cluster.replicas)].leer("usuario:42")]
            leido, lsn_leido = max(respuestas, key=lambda r: r[1])
        else:
            raise ValueError(estrategia)

        if leido != valor:
            violaciones_lectura_propia += 1
        if lsn_leido < lsn:
            lecturas_obsoletas += 1
        if lsn_leido < ultimo_lsn_visto:
            # El cliente ve el tiempo ir hacia atras: leyo un seguidor mas
            # atrasado que el de la peticion anterior.
            lecturas_no_monotonas += 1
        ultimo_lsn_visto = max(ultimo_lsn_visto, lsn_leido)

    return {
        "sin lectura propia": violaciones_lectura_propia,
        "obsoletas": lecturas_obsoletas,
        "no monotonas": lecturas_no_monotonas,
        "esperas": esperas,
    }


def medir_retraso_bajo_carga() -> list[tuple[int, int]]:
    """Retraso del seguidor mas lento a medida que entran escrituras."""
    cluster = Cluster()
    medidas = []
    for i in range(12):
        cluster.escribir("metrica", f"v{i}")
        cluster.avanzar(1)
        pendientes = len(cluster.registro) - min(len(r.aplicadas) for r in cluster.replicas)
        medidas.append((cluster.tick, pendientes))
    return medidas


def main() -> None:
    print(f"Lider + {len(RETRASOS)} seguidores · retrasos: "
          + ", ".join(f"{n} = {t} ticks" for n, t in RETRASOS.items()))
    print(f"{CLIENTES} escrituras, cada una releida un tick despues.\n")

    print(f"{'estrategia de lectura':<24} {'sin lectura propia':>19} {'obsoletas':>10} "
          f"{'no monotonas':>13} {'esperas':>8}")
    informe = {}
    for estrategia in ("lider", "seguidor", "sesion", "quorum"):
        r = escenario(estrategia)
        informe[estrategia] = r
        print(f"{estrategia:<24} {r['sin lectura propia']:>19} {r['obsoletas']:>10} "
              f"{r['no monotonas']:>13} {r['esperas']:>8}")

    # 1. Leer de un seguidor rompe la lectura de lo propio: el cliente no ve lo
    #    que acaba de escribir. Es el fallo que la gente descubre en produccion.
    assert informe["seguidor"]["sin lectura propia"] == CLIENTES, (
        "leer del seguidor deberia devolver siempre una version anterior con estos retrasos")
    assert informe["seguidor"]["obsoletas"] == CLIENTES

    # 2. El reparto entre seguidores con retrasos distintos hace que el tiempo
    #    retroceda para el cliente: lecturas no monotonas.
    assert informe["seguidor"]["no monotonas"] > 0, "el reparto deberia producir retrocesos"

    # 3. Las tres correcciones sostienen la lectura de lo propio.
    for estrategia in ("lider", "sesion", "quorum"):
        assert informe[estrategia]["sin lectura propia"] == 0, (
            f"{estrategia}: deberia garantizar leer lo que uno acaba de escribir")
        assert informe[estrategia]["no monotonas"] == 0, f"{estrategia}: retroceso detectado"

    # 4. La garantia de sesion no sale gratis: se paga esperando.
    assert informe["sesion"]["esperas"] > 0, "la garantia de sesion deberia costar espera"
    assert informe["lider"]["esperas"] == 0

    medidas = medir_retraso_bajo_carga()
    print("\nEscrituras pendientes de aplicar en el seguidor mas lento")
    print("  tick:      " + " ".join(f"{t:>3}" for t, _ in medidas))
    print("  pendientes:" + " ".join(f"{p:>3}" for _, p in medidas))
    # La cola se estabiliza en `retraso - 1`, no en `retraso`: la escritura del
    # tick en curso todavia no ha tenido ocasion de viajar. Ese uno de
    # diferencia es justo el tipo de detalle que un panel de monitorizacion
    # muestra y nadie sabe explicar.
    estable = {p for _, p in medidas[6:]}
    esperado = RETRASOS["seguidor-b"] - 1
    assert estable == {esperado}, (
        f"con retraso constante, la cola deberia estabilizarse en {esperado}, no en {estable}")

    print("\nConclusion, limitada a este modelo: leer de un seguidor no es una optimizacion")
    print("gratuita, es un cambio de garantia. Se recupera leyendo del lider (mas carga),")
    print("esperando la posicion propia (mas latencia) o exigiendo quorum (mas peticiones).")
    print("REPLICATION_LAB_OK")


if __name__ == "__main__":
    main()
