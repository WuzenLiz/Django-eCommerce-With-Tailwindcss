from django.db import models
from saleproduct.models import Product
from accounts.models import CustomUserAccount as Account

# Create your models here.
class Cart(models.Model):
 cart_id = models.CharField(max_length=250, blank=True)
 date_added = models.DateField(auto_now_add=True)

 class Meta:
  db_table = 'cart'
  ordering = ['date_added']

 def __str__(self):
  return self.cart_id

class CartItem(models.Model):
 user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
 product = models.ForeignKey(Product, on_delete=models.CASCADE)
 cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
 quantity = models.IntegerField()
 is_active = models.BooleanField(default=True)

 class Meta:
  db_table = 'cartItem'

 def sub_total(self):
  return self.product.price * self.quantity

 def __str__(self):
  return self.product