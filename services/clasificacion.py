from django.db.models import Q
from apps.equipos.models import Equipo
from apps.partidos.models import Partido


def calcular_clasificacion():

    tabla = defaultdict(lambda: {
        "equipo": None,
        "pj": 0,
        "pg": 0,
        "pp": 0,
        "gf": 0,
        "gc": 0,
        "pts": 0
    })

    partidos = Partido.objects.filter(estado="finalizado")

    for partido in partidos:

        local = partido.local
        visitante = partido.visitante

        gl = partido.goles_local
        gv = partido.goles_visitante

        tabla[local.id]["equipo"] = local
        tabla[visitante.id]["equipo"] = visitante

        tabla[local.id]["pj"] += 1
        tabla[visitante.id]["pj"] += 1

        tabla[local.id]["gf"] += gl
        tabla[local.id]["gc"] += gv

        tabla[visitante.id]["gf"] += gv
        tabla[visitante.id]["gc"] += gl

        # GANADOR EN TIEMPO NORMAL
        if gl > gv:

            tabla[local.id]["pg"] += 1
            tabla[local.id]["pts"] += 3

            tabla[visitante.id]["pp"] += 1

        elif gv > gl:

            tabla[visitante.id]["pg"] += 1
            tabla[visitante.id]["pts"] += 3

            tabla[local.id]["pp"] += 1

        # EMPATE -> PENALTIS
        else:

            pl = partido.penaltis_local
            pv = partido.penaltis_visitante

            if pl > pv:

                tabla[local.id]["pg"] += 1
                tabla[local.id]["pts"] += 2

                tabla[visitante.id]["pp"] += 1
                tabla[visitante.id]["pts"] += 1

            else:

                tabla[visitante.id]["pg"] += 1
                tabla[visitante.id]["pts"] += 2

                tabla[local.id]["pp"] += 1
                tabla[local.id]["pts"] += 1

    clasificacion = list(tabla.values())

    clasificacion.sort(
        key=lambda x: (x["pts"], x["gf"] - x["gc"], x["gf"]),
        reverse=True
    )

    return clasificacion