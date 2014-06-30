# -*- coding: utf-8 -*-
from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()
debug = False


@register.filter
@stringfilter
def remove_auth(value):
    if debug:
        print value

    if value == u"Auth":
        return u"Autorización"
    elif value == u"auth":
        return u"autorización"
    elif value == u"Administración de Auth":
        return u"Administración de Permisos"
    else:
        return value


@register.filter
@stringfilter
def remove_staff_or_su(value):
    if value == "es staff":
        return "staff"
    elif value == "es superusuario":
        return "super usuario"
    else:
        return value