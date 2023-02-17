from django.db import models
from .model_manage import *
from django.utils.text import slugify
from django.utils.translation import gettext_lazy as _
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError

# Create your models here.
class HomeBannerContent(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to="res/image/home_banner", blank=True, null=True)
    link = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Home Banner Content"
        verbose_name_plural = "Home Banner Contents"

    def __str__(self):
        return self.title


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField(
        "Meta Keywords",
        max_length=255,
        help_text=_("Comma-delimited set of SEO keywords for meta tag"),
        blank=True,
        null=True,
    )
    meta_description = models.CharField(
        "Meta Description",
        max_length=255,
        help_text=_("Content for description meta tag"),
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category_image = models.ImageField(upload_to="res/image/categories", blank=True)
    category_icon = models.TextField(
        _("Category Icon"),
        blank=True,
        help_text=_(
            "Category Icon (Font Awesome) - Example: fa fa-home find more at https://fontawesome.com/icons/"
        ),
    )

    @property
    def get_number_of_products(self):
        return self.product_set.filter(is_active=True).count()

    class Meta:
        ordering = ("name",)
        verbose_name = "category"
        verbose_name_plural = "categories"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("category", args=[self.slug])

class Brand(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    is_featured = models.BooleanField(default=False)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    meta_keywords = models.CharField(
        "Meta Keywords",
        max_length=255,
        help_text=_("Comma-delimited set of SEO keywords for meta tag"),
        blank=True,
        null=True,
    )
    meta_description = models.CharField(
        "Meta Description",
        max_length=255,
        help_text=_("Content for description meta tag"),
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    brand_image = models.ImageField(upload_to="res/image/brands", blank=True)

    @property
    def get_number_of_products(self):
        return self.product_set.filter(is_active=True).count()

    class Meta:
        ordering = ("name",)
        verbose_name = "brand"
        verbose_name_plural = "brands"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("brand", args=[self.slug])


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=255, unique=True)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    description = models.TextField()
    main_image = models.ImageField(
        upload_to="res/image/products", verbose_name="Main Image"
    )
    meta_keywords = models.CharField(
        max_length=255,
        help_text="Comma-delimited set of SEO keywords for meta tag",
        blank=True,
        null=True,
    )
    meta_description = models.CharField(
        max_length=255,
        help_text="Content for description meta tag",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    # SubCategory = models.ForeignKey(SubCategory, on_delete=models.CASCADE,parent_link=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "product"
        verbose_name_plural = "products"

    # using for manage product
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
        return reverse("product_detail", args=[self.slug])

    @property
    def stock(self):
        return self.variants.aggregate(models.Sum("quantity"))["quantity__sum"]

    @property
    def highest_price(self):
        return self.variants.aggregate(models.Max("price"))["price__max"]

    @property
    def lowest_price(self):
        return self.variants.aggregate(models.Min("price"))["price__min"]

    @property
    def is_best_seller(self):
        # count the number of order
        return self.variants.aggregate(models.Sum("quantity"))["quantity__sum"] > 0

    @property
    def is_out_of_stock(self):
        return self.stock <= 0

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

    def related_products(self):
        try:
            return self.categories.products.filter(is_active=True)
        except Product.DoesNotExist:
            return None

    def attributes(self):
        try:
            return self.attributes.filter(is_active=True)
        except ProductAttribute.DoesNotExist:
            return None
    
    def main_variant(self):
        try:
            return self.variants.get(is_main=True)
        except ProductVariant.DoesNotExist:
            return None

class ProductVariants(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="variants",
    )
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

    is_main = models.BooleanField(default=False)

    objects = VariantManager()

    class Meta:
        ordering = ("name",)
        verbose_name = "product variant"
        verbose_name_plural = "product variants"

    def __str__(self):
        return self.name

    @property
    def sale_price(self):
        return self.price - (self.price * self.saleoff / 100)

    def create_variant(self, product, name, sku, price, saleoff, quantity):
        variant = self.model(
            product=product,
            name=name,
            sku=sku,
            price=price,
            saleoff=saleoff,
            quantity=quantity,
        )
        variant.save(using=self._db)
        return variant

class ProductImage(models.Model):
    # many image for one product
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="images"
    )
    image = models.ImageField(upload_to="res/image/products")
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(default=timezone.now)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ("date_created",)
        verbose_name = "product image"
        verbose_name_plural = "product images"

class ProductAttribute(models.Model):
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="attributes"
    )
    name = models.CharField(max_length=50)
    value = models.CharField(max_length=50)

    class Meta:
        ordering = ("name",)
        verbose_name = "product attribute"
        verbose_name_plural = "product attributes"

    def __str__(self):
        return self.name