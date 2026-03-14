from collections import defaultdict
from .models import Partido


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

    partidos = Partido.objects.filter(
        estado=Partido.Estado.FINALIZADO
    ).select_related("local", "visitante")

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

        if partido.resultado == partido.Resultado.LOCAL:
            tabla[local.id]["pg"] += 1
            tabla[local.id]["pts"] += 3
            tabla[visitante.id]["pp"] += 1

        elif partido.resultado == partido.Resultado.VISITANTE:
            tabla[visitante.id]["pg"] += 1
            tabla[visitante.id]["pts"] += 3
            tabla[local.id]["pp"] += 1

        elif partido.resultado == partido.Resultado.PENALES_LOCAL:
            tabla[local.id]["pg"] += 1
            tabla[local.id]["pts"] += 2
            tabla[visitante.id]["pp"] += 1
            tabla[visitante.id]["pts"] += 1

        elif partido.resultado == partido.Resultado.PENALES_VISITANTE:
            tabla[visitante.id]["pg"] += 1
            tabla[visitante.id]["pts"] += 2
            tabla[local.id]["pp"] += 1
            tabla[local.id]["pts"] += 1

    clasificacion = list(tabla.values())

    # separar por grupos
    grupo_a = [x for x in clasificacion if x["equipo"].grupo == "A"]
    grupo_b = [x for x in clasificacion if x["equipo"].grupo == "B"]

    grupo_a.sort(key=lambda x: (x["pts"], x["gf"]-x["gc"], x["gf"]), reverse=True)
    grupo_b.sort(key=lambda x: (x["pts"], x["gf"]-x["gc"], x["gf"]), reverse=True)

    return grupo_a, grupo_b