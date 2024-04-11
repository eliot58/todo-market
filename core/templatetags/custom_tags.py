from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, a):
    return value * a


@register.filter(name='time')
def time(value):
    return value.strftime("%H:%M")
