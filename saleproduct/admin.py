from django.contrib import admin
from .models import *
# Register your models here.
class CategoryAdmin(admin.ModelAdmin):
 prepopulated_fields = {'slug': ('name',)}
 list_display = ['name', 'slug']
admin.site.register(Category, CategoryAdmin)

class BrandAdmin(admin.ModelAdmin):
 prepopulated_fields = {'slug': ('name',)}
 list_display = ['name', 'slug']
admin.site.register(Brand, BrandAdmin)

class ProductVariantsAdmin(admin.TabularInline):
 model = ProductVariants
 extra = 0
 list_display = ['name', 'sku', 'price', 'saleoff', 'is_active', 'is_bestseller', 'is_featured', 'quantity']
 list_filter = ['is_active', 'is_bestseller', 'is_featured']
 list_editable = ['is_active', 'is_bestseller', 'is_featured']

class ProductImageAdmin(admin.TabularInline):
 model = ProductImage
 extra = 0
 list_display = ['image', 'is_active', 'is_main']
 list_filter = ['is_active', 'is_main']
 list_editable = ['is_active', 'is_main']


class ProductAdmin(admin.ModelAdmin):
 prepopulated_fields = {'slug': ('name',)}
 list_display = ['name', 'slug', 'brand', 'is_active']
 list_filter = ['is_active', 'brand']
 list_editable = ['is_active']
 filter_horizontal = ('categories',)
 inlines = [ProductVariantsAdmin, ProductImageAdmin]
 # fields = ['name', 'slug', 'brand', 'description', 'categories', 'variants', 'images', 'is_active', 'meta_keywords', 'meta_description']
admin.site.register(Product, ProductAdmin)
