from django.db import models

# Create your models here.

from django.db import models


class Equipo(models.Model):
    escudo = models.ImageField(
        upload_to="escudos/",
        null=True,
        blank=True
    )
    class Grupo(models.TextChoices):
        A = "A", "Grupo A"
        B = "B", "Grupo B"
    nombre = models.CharField(
        max_length=100,
        unique=True
    )
    apodo = models.CharField(
        max_length=100,
        blank=True
    )
    grupo = models.CharField(
        max_length=1,
        choices=Grupo.choices
    )

    creado = models.DateTimeField(auto_now_add=True)
    actualizado = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["nombre"]

    def __str__(self):
        return self.nombre