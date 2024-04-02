from django import template

register = template.Library()

@register.filter
def hide_password(value):
    return '*' * len(value)
