from django import template

register = template.Library()


@register.filter
def split_last(value):
    return value.split('.')[-1]