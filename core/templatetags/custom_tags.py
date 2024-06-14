from django import template

register = template.Library()

@register.filter(name='multiply')
def multiply(value, a):
    return value * a


@register.filter(name='time')
def time(value):
    return value.strftime("%H:%M")

@register.filter(name='join_tag_names')
def join_tag_names(tags):
    return ', '.join(tag.name for tag in tags)