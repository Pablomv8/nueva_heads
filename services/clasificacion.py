from django.db.models import Q
from apps.equipos.models import Equipo
from apps.partidos.models import Partido


def calcular_clasificacion(grupo: str):
    """
    Devuelve la tabla ordenada por:
    - puntos
    - diferencia de goles
    - goles a favor
    """

    equipos = Equipo.objects.filter(grupo=grupo)

    tabla = []

    for equipo in equipos:
        partidos = Partido.objects.filter(
            Q(local=equipo) | Q(visitante=equipo),
            estado=Partido.Estado.FINALIZADO
        )

        puntos = 0
        goles_favor = 0
        goles_contra = 0
        jugados = 0

        for partido in partidos:
            jugados += 1

            if partido.local == equipo:
                goles_favor += partido.goles_local
                goles_contra += partido.goles_visitante

                if partido.resultado == Partido.Resultado.LOCAL:
                    puntos += 3
                elif partido.resultado == Partido.Resultado.EMPATE:
                    puntos += 1

            else:
                goles_favor += partido.goles_visitante
                goles_contra += partido.goles_local

                if partido.resultado == Partido.Resultado.VISITANTE:
                    puntos += 3
                elif partido.resultado == Partido.Resultado.EMPATE:
                    puntos += 1

        tabla.append({
            "equipo": equipo,
            "puntos": puntos,
            "jugados": jugados,
            "gf": goles_favor,
            "gc": goles_contra,
            "dg": goles_favor - goles_contra,
        })

    # Orden oficial
    tabla_ordenada = sorted(
        tabla,
        key=lambda x: (-x["puntos"], -x["dg"], -x["gf"])
    )

    return tabla_ordenada