from django.contrib import admin
from .models import *
from django import forms
from django.utils.translation import gettext_lazy as _


# Register your models here.
class BrandAdmin(admin.ModelAdmin):
 prepopulated_fields = {'slug': ('name',)}
 list_display = ['name', 'slug']
admin.site.register(Brand, BrandAdmin)

class ProductVariantsFormset(forms.BaseInlineFormSet):
 def is_valid(self):
  result = super(ProductVariantsFormset, self).is_valid()
  for form in self.forms:
   if not form.is_valid():
    return False
  return result

 def clean(self):
  super(ProductVariantsFormset, self).clean()
  if any(self.errors):
   return
  is_main = False
  for form in self.forms:
   if form.cleaned_data.get('is_main'):
    is_main = True
    break
   # if there is no main variant, raise an error
  if not is_main:
   raise forms.ValidationError(_('At least one variant must be marked as main'))
  

class ProductVariantsAdmin(admin.StackedInline):
 model = ProductVariants
 extra = 0
 formset = ProductVariantsFormset
 list_display = ['name', 'sku', 'price', 'saleoff', 'is_active', 'is_bestseller', 'is_featured', 'quantity']
 list_filter = ['is_active', 'is_bestseller', 'is_featured']
 list_editable = ['is_active', 'is_bestseller', 'is_featured']

class ProductImageAdmin(admin.StackedInline):
 model = ProductImage
 extra = 0
 list_display = ['image', 'is_active', 'is_main']
 list_filter = ['is_active', 'is_main']
 list_editable = ['is_active', 'is_main']

class ProductAttributeAdmin(admin.StackedInline):
 model = ProductAttribute
 extra = 0
 list_display = ['name', 'value']
 list_filter = ['name']
 list_editable = ['value']


class ProductAdmin(admin.ModelAdmin):
 prepopulated_fields = {'slug': ('name',)}
 list_display = ['name', 'slug', 'brand', 'is_active']
 list_filter = ['is_active', 'brand']
 list_editable = ['is_active']
 inlines = [ProductVariantsAdmin, ProductImageAdmin, ProductAttributeAdmin]
 # fields = ['name', 'slug', 'brand', 'description', 'categories', 'variants', 'images', 'is_active', 'meta_keywords', 'meta_description']

admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
 prepopulated_fields = {'slug': ('name',)}
 list_display = ['name', 'slug']
admin.site.register(Category, CategoryAdmin)