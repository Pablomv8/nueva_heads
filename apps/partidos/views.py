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