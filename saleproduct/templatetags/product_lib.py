from django import template
from django.utils.formats import number_format
from django.utils.formats import localize
register = template.Library()

@register.simple_tag
def define(val=None):
  return val

@register.filter
def currency(value):
  # to vietnamese currency
  print(localize(value))
  if value == 0:
    return 'Liên hệ'
  return number_format(value, decimal_pos=0, use_l10n=True, force_grouping=True) + 'đ'