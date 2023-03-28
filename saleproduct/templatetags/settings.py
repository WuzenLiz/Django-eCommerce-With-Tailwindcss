from django.conf import settings
from django import template

register = template.Library()
#Settings variables loading tag
@register.simple_tag(name='settings')
def settings_value(name):
    return settings.__getattr__(name)

@register.simple_tag(name='get_value')
def get_value(d): # get value from tuple(key, value)
    return d[1]

@register.simple_tag(name='get_key')
def get_key(d): # get key from tuple(key, value)
    return d[0]