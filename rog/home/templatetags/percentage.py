from django import template

register = template.Library()


@register.filter
def percentage(value, arg):
    print(value)
    print(arg)
    return float(value) * (arg / 100)
