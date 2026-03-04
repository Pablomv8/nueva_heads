from django.contrib import admin
from .models import Jornada, Partido

@admin.register(Jornada)
class JornadaAdmin(admin.ModelAdmin):
    list_display = ("numero", "fecha_inicio")

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ("local", "visitante", "jornada", "fecha", "estado", "resultado")