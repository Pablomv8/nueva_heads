from django.db import models

# Create your models here.
from django.db import models
from apps.equipos.models import Equipo


class Jornada(models.Model):
    numero = models.PositiveIntegerField(unique=True)
    fecha_inicio = models.DateField()

    creado = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["numero"]

    def __str__(self):
        return f"Jornada {self.numero}"


class Partido(models.Model):

    class Estado(models.TextChoices):
        SIN_COMENZAR = "sin_comenzar", "Sin comenzar"
        FINALIZADO = "finalizado", "Finalizado"

    class Resultado(models.TextChoices):
        LOCAL = "local", "Victoria local"
        VISITANTE = "visitante", "Victoria visitante"
        EMPATE = "empate", "Empate"
        PENALES_LOCAL = "penales_local", "Penales local"
        PENALES_VISITANTE = "penales_visitante", "Penales visitante"

    jornada = models.ForeignKey(
        Jornada,
        on_delete=models.CASCADE,
        related_name="partidos"
    )

    local = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name="partidos_local"
    )

    visitante = models.ForeignKey(
        Equipo,
        on_delete=models.CASCADE,
        related_name="partidos_visitante"
    )

    fecha = models.DateTimeField()

    goles_local = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    goles_visitante = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    penaltis_local = models.PositiveIntegerField(
    null=True,
    blank=True
    )

    penaltis_visitante = models.PositiveIntegerField(
    null=True,
    blank=True
    )   

    estado = models.CharField(
        max_length=20,
        choices=Estado.choices,
        default=Estado.SIN_COMENZAR
    )

    resultado = models.CharField(
        max_length=20,
        choices=Resultado.choices,
        null=True,
        blank=True
    )

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["fecha"]
        constraints = [
            models.UniqueConstraint(
                fields=["jornada", "local", "visitante"],
                name="unique_partido_por_jornada"
            )
        ]

    def __str__(self):
        return f"{self.local} vs {self.visitante}"

    def save(self, *args, **kwargs):

        if self.estado == self.Estado.FINALIZADO:

            if self.goles_local is not None and self.goles_visitante is not None:

                # victoria directa
                if self.goles_local > self.goles_visitante:
                    self.resultado = self.Resultado.LOCAL

                elif self.goles_local < self.goles_visitante:
                    self.resultado = self.Resultado.VISITANTE

                # empate -> penaltis
                else:

                    if self.penaltis_local is not None and self.penaltis_visitante is not None:

                        if self.penaltis_local > self.penaltis_visitante:
                            self.resultado = self.Resultado.PENALES_LOCAL

                        elif self.penaltis_visitante > self.penaltis_local:
                            self.resultado = self.Resultado.PENALES_VISITANTE

                    else:
                        self.resultado = self.Resultado.EMPATE

        super().save(*args, **kwargs)