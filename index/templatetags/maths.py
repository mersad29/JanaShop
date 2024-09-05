from django import template

register = template.Library()

@register.filter
def to_range(value):
    """Converts an integer into a range up to that integer."""
    return range(value)