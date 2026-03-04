from django.shortcuts import render

# Create your views here.
from django.shortcuts import render
from services.clasificacion import calcular_clasificacion


def tabla_grupo(request, grupo):
    tabla = calcular_clasificacion(grupo)
    return render(request, "equipos/tabla.html", {"tabla": tabla})