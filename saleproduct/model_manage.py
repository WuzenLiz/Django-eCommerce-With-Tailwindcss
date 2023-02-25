from django.db import models

class ProductManager(models.Manager):
 def get_queryset(self):
  return super(ProductManager, self).get_queryset().filter(is_active=True)

 def search(self, query):
  return self.get_queryset().filter(
   models.Q(name__icontains=query) |
   models.Q(description__icontains=query) |
   models.Q(meta_keywords__icontains=query) |
   models.Q(meta_description__icontains=query)
  )

  def get_by_category(self, category):
   return self.get_queryset().filter(categories__id=category.id) 

  def get_by_brand(self, brand):
   return self.get_queryset().filter(brand__id=brand.id)

  def get_by_id(self, id):
   return self.get_queryset().filter(id=id)

  def get_by_slug(self, slug):
   return self.get_queryset().filter(slug=slug)

  def get_by_price(self, price):
   return self.get_queryset().filter(price=price)

  def get_by_price_range(self, min, max):
   return self.get_queryset().filter(price__gte=min, price__lte=max)

class VariantManager(models.Manager):
 def get_queryset(self):
  return super(VariantManager, self).get_queryset().filter(is_active=True)

 def get_by_id(self, id):
  return self.get_queryset().filter(id=id)

 def get_by_product(self, product):
  return self.get_queryset().filter(product__id=product.id)

 def get_by_price(self, price):
  return self.get_queryset().filter(price=price)

 def get_by_price_range(self, min, max):
  return self.get_queryset().filter(price__gte=min, price__lte=max)

 def sync_variants(self, product, variants):
  for variant in variants:
   try:
    v = self.get(id=variant['id'])
    v.sku = variant['sku']
    v.price = variant['price']
    v.save()
   except ProductVariant.DoesNotExist:
    v = ProductVariant()
    v.product = product
    v.sku = variant['sku']
    v.price = variant['price']
    v.save()