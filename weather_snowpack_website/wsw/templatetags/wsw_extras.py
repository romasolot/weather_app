from django import template

register = template.Library()

@register.filter
def dict_key_value(dict, key):
    return dict[key]