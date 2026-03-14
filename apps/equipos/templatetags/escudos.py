from django import template

register = template.Library()


@register.simple_tag
def escudo_equipo(equipo):

    if equipo.escudo:
        return equipo.escudo.url

    return "/media/escudos/default.png"