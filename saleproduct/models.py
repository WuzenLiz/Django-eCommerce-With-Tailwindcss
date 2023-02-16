from django.db import models
from .model_manage import *
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls import reverse

# Create your models here.
class HomeBannerContent(models.Model):
  title = models.CharField(max_length=255, blank=True, null=True)
  subtitle = models.CharField(max_length=255, blank=True, null=True)
  image = models.ImageField(upload_to='res/image/home_banner', blank=True, null=True)
  link = models.CharField(max_length=255, blank=True, null=True)
  is_active = models.BooleanField(default=True)
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  
  class Meta:
    ordering = ('-created_at',)
    verbose_name = 'Home Banner Content'
    verbose_name_plural = 'Home Banner Contents'
  
  def __str__(self):
    return self.title


class Category(models.Model):
 name = models.CharField(max_length=100)
 slug = models.SlugField(max_length=100, unique=True)
 description = models.TextField(blank=True)
 is_active = models.BooleanField(default=True)
 meta_keywords = models.CharField("Meta Keywords", max_length=255, help_text=_(u'Comma-delimited set of SEO keywords for meta tag'),blank=True, null=True)
 meta_description = models.CharField("Meta Description", max_length=255, help_text=_(u'Content for description meta tag'), blank=True, null=True)
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateTimeField(auto_now=True)
 category_image = models.ImageField(upload_to='res/image/categories', blank=True)
 category_icon = models.TextField(_("Category Icon"), blank=True, help_text=_("Category Icon (Font Awesome) - Example: fa fa-home find more at https://fontawesome.com/icons/"))

 class Meta:
  ordering = ('name',)
  verbose_name = 'category'
  verbose_name_plural = 'categories'

 def __str__(self):
  return self.name

 def get_absolute_url(self):
  return reverse('category', args=[self.slug])



class Brand(models.Model):
 name = models.CharField(max_length=100)
 slug = models.SlugField(max_length=100, unique=True)
 is_featured = models.BooleanField(default=False)
 description = models.TextField(blank=True)
 is_active = models.BooleanField(default=True)
 meta_keywords = models.CharField("Meta Keywords", max_length=255, help_text=_(u'Comma-delimited set of SEO keywords for meta tag'),blank=True, null=True)
 meta_description = models.CharField("Meta Description", max_length=255, help_text=_(u'Content for description meta tag'), blank=True, null=True)
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateTimeField(auto_now=True)
 brand_image = models.ImageField(upload_to='res/image/brands', blank=True)

 class Meta:
  ordering = ('name',)
  verbose_name = 'brand'
  verbose_name_plural = 'brands'

 def __str__(self):
  return self.name

 def get_absolute_url(self):
  return reverse('brand', args=[self.slug])

class Product(models.Model):
 name = models.CharField(max_length=255, unique=True)
 slug = models.SlugField(max_length=255, unique=True)
 brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
 description = models.TextField()
 main_image = models.ImageField(upload_to='res/image/products', verbose_name='Main Image', blank=True)
 meta_keywords = models.CharField(max_length=255, help_text='Comma-delimited set of SEO keywords for meta tag', blank=True, null=True)
 meta_description = models.CharField(max_length=255, help_text='Content for description meta tag', blank=True, null=True)
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateTimeField(auto_now=True)
 categories = models.ManyToManyField(Category)
 is_active = models.BooleanField(default=True)

 class Meta:
  ordering = ('-created_at',)
  verbose_name = 'product'
  verbose_name_plural = 'products'
 
 #using for manage product
 objects = ProductManager()

 def save(self, *args, **kwargs):
  self.variants.product = self
  self.images.product = self
  if not self.id:
   self.slug = slugify(self.name)
  if self.is_active == False:
   self.is_bestseller = False
   self.is_featured = False
  super(Product, self).save(*args, **kwargs)

 def __str__(self):
  return self.name

 def get_absolute_url(self):
  return reverse('product_detail', args=[self.slug])

 @property
 def highest_price(self):
  return self.variants.aggregate(models.Max('price'))['price__max']
 
 @property
 def lowest_price(self):
  return self.variants.aggregate(models.Min('price'))['price__min']
 
 @property
 def get_price(self):
  #get the lowest sale price sale_price
  return self.variants.aggregate(models.Min('sale_price'))['price__min']

 @property
 def get_sale_price(self):
  #get the lowest sale price sale_price
  return self.variants.aggregate(models.Min('sale_price'))['sale_price__min']

 @property
 def has_saleoff(self):
  if self.variants.aggregate(models.Min('sale_price'))['sale_off__min'] > 0:
   return True

 def images(self):
  try:
   return self.images.filter(is_active=True)
  except ProductImage.DoesNotExist:
   return None
 
 def variants(self):
  try:
   return self.variants.filter(is_active=True)
  except ProductVariant.DoesNotExist:
   return None

class ProductVariants(models.Model):
 product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants',)
 name = models.CharField(max_length=50)
 sku = models.CharField(max_length=50)
 price = models.DecimalField(max_digits=9, decimal_places=2)
 saleoff = models.IntegerField(default=0)
 is_active = models.BooleanField(default=True)
 is_bestseller = models.BooleanField(default=False)
 is_featured = models.BooleanField(default=False)
 quantity = models.IntegerField()
 created_at = models.DateTimeField(auto_now_add=True)
 updated_at = models.DateTimeField(auto_now=True)

 objects = VariantManager()

 class Meta:
  ordering = ('name',)
  verbose_name = 'product variant'
  verbose_name_plural = 'product variants'

 def __str__(self):
  return self.name
 
 @property
 def sale_price(self):
  if self.saleoff > 0:
   return self.price - (self.price * self.saleoff / 100)
  else:
   return self.price

  def create_variant(self, product, name, sku, price, saleoff, quantity):
   variant = self.model(
    product=product,
    name=name,
    sku=sku,
    price=price,
    saleoff=saleoff,
    quantity=quantity
   )
   variant.save(using=self._db)
   return variant

class ProductImage(models.Model):
 # many image for one product
 product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
 image = models.ImageField(upload_to='res/image/products')
 is_active = models.BooleanField(default=True)
 is_main = models.BooleanField(default=False)

 class Meta:
  ordering = ('is_main',)
  verbose_name = 'product image'
  verbose_name_plural = 'product images'