from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from django.utils import timezone
from .models import Jornada


def home(request):
    hoy = timezone.now().date()

    # Buscar la próxima jornada
    proxima_jornada = (
        Jornada.objects
        .filter(fecha_inicio__gt=hoy)
        .order_by("fecha_inicio")
        .first()
    )

    partidos = []

    if proxima_jornada:
        partidos = proxima_jornada.partidos.select_related("local", "visitante")

    context = {
        "jornada": proxima_jornada,
        "partidos": partidos,
    }

    return render(request, "home.html", context)

from django.shortcuts import render
from .services import calcular_clasificacion


def clasificacion_view(request):

    grupo_a, grupo_b = calcular_clasificacion()

    context = {
        "grupo_a": grupo_a,
        "grupo_b": grupo_b
    }

    return render(request, "clasificacion.html", context)


def resultados_view(request):

    jornadas = Jornada.objects.all()

    jornada_id = request.GET.get("jornada")

    if jornada_id:
        jornada = Jornada.objects.get(id=jornada_id)
    else:
        jornada = jornadas.first()

    partidos = jornada.partidos.select_related(
        "local",
        "visitante"
    ) if jornada else []
    partidos_a = partidos.filter(local__grupo="A")
    partidos_b = partidos.filter(local__grupo="B")
    context = {
        "jornada": jornada,
        "jornadas": jornadas,
        "partidos": partidos,
        "partidos_a": partidos_a,
        "partidos_b": partidos_b,
    }

    return render(request, "resultados.html", context)