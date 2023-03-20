from django.conf import settings
from django import template

register = template.Library()
#Settings variables loading tag
@register.simple_tag(name='settings')
def settings_value(name):
    return settings.__getattr__(name)