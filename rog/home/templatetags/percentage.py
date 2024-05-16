from django import template

register = template.Library()


@register.filter
def percentage(value, arg):
    print(value)
    print(arg)
    return float(value) * (arg / 100)


@register.filter
def multiply(value, arg):
    return int(value) * int(arg)
