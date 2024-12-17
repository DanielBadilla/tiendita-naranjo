from django import template
register = template.Library()

@register.filter
def custom_zip(value, arg):
    return zip(value, arg)
