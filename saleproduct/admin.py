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

 def save(self, commit=True):
  result = super(ProductVariantsFormset, self).save(commit=False)
  for form in self.forms:
   if commit:
    form.save()
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
 
 def save_formset(self, request, form, formset, change):
  if formset.model == ProductVariants:
   instances = formset.save(commit=False)
   for instance in instances:
    instance.product = form.instance
    instance.save()
  else:
   formset.save()

 # fields = ['name', 'slug', 'brand', 'description', 'categories', 'variants', 'images', 'is_active', 'meta_keywords', 'meta_description']

admin.site.register(Product, ProductAdmin)

class CategoryAdmin(admin.ModelAdmin):
 prepopulated_fields = {'slug': ('name',)}
 list_display = ['name', 'slug','is_active', 'meta_keywords', 'meta_description', 'created_at', 'updated_at','is_active']
 list_filter = ['name', 'is_active']
 def get_form(self, request, obj=None, **kwargs):
  kwargs['widgets'] = {
    'category_icon': forms.TextInput(attrs={'placeholder': 'fa fa-home'}),
  }
  return super(CategoryAdmin, self).get_form(request, obj, **kwargs)
admin.site.register(Category, CategoryAdmin)

class HomeBannerContentAdmin(admin.ModelAdmin):
 list_display = ['title','subtitle','image','link','is_active']
admin.site.register(HomeBannerContent, HomeBannerContentAdmin)