from django.urls import path
from . import views
from .views import home, clasificacion_view, resultados_view

urlpatterns = [
     path("", home, name="home"),
     path("clasificacion/", clasificacion_view, name="clasificacion"),
     path("resultados",resultados_view, name="resultados"),
]