from django.db import models
from saleproduct.models import Product, ProductVariants
from accounts.models import CustomUserAccount as Account
from accounts.models import userAddressBook


class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True)

    @property
    def id(self):
        return self.cart_id
    
    @property
    def total(self):
        return sum(item.cost for item in self.cartitem_set.all())
    
    @property
    def tax(self):
        return (self.total * 2) /100

    @property
    def grand_total(self):
        return self.total + self.tax

    class Meta:
        db_table = 'cart'
        ordering = ['date_added']

    def __str__(self):
        return self.cart_id



class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(
        ProductVariants, on_delete=models.CASCADE, null=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = 'cartItem'

    @property
    def cost(self):
        return self.product.price * self.quantity
    
    @property
    def total_item(self):
        return self.count() * self.quantity

    def __str__(self):
        return self.product

Payment_method = (
    ('COD', 'Thanh toán khi nhận hàng'),
    # ('VNPAY', 'Thanh toán qua VNPAY'),
)

class PayOrder(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment_method = models.CharField(max_length=10, choices=Payment_method, default='COD')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'payments'
        ordering = ['-created_at']

    def payment_method(self):
        return self.payment_method

    def __str__(self):
        return f'Payment {self.id}'


class Order(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
    )
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    payment = models.CharField(max_length=9000, choices=Payment_method, default='COD')
    receiver_address = models.ForeignKey(userAddressBook, on_delete=models.CASCADE, null=True, blank=True)
    order_note = models.CharField(max_length=100, blank=True)
    order_total = models.FloatField()
    status = models.CharField(max_length=100, choices=STATUS, default='New')
    is_ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'orders'
        ordering = ['-created_at']

    def __str__(self):
        return f'Order {self.id}'

class OrderItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariants, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.FloatField()
    ordered = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'order_items'

    def __str__(self):
        return self.product

class OrderProduct(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    product = models.ForeignKey(ProductVariants, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    product_price = models.FloatField()
    ordered = models.BooleanField(default=False)

    class Meta:
        db_table = 'order_products'
