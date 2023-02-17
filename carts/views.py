from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from saleproduct.models import Product, ProductVariants
from .models import Cart, CartItem
# Create your views here.

def _cart_id(request):
 cart = request.session.session_key
 if not cart:
  cart = request.session.create()
 return cart

def add_cart(request, product_id):
 current_user = request.user
 product = Product.objects.get(id=product_id)
 if current_user.is_authenticated:
  product_variation = []
  if request.method == 'POST':
   for item in request.POST:
    key = item
    value = request.POST[key]
    try:
     variation = ProductVariants.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
     product_variation.append(variation)
    except:
     pass
   is_cart_item_exists = CartItem.objects.filter(product=product, user=current_user, variation__id__in=product_variation).exists()
   if is_cart_item_exists:
    cart_item = CartItem.objects.filter(product=product, user=current_user)
    existing_var_list = []
    id = []
    for item in cart_item:
     existing_variation = item.variation.all()
     existing_var_list.append(list(existing_variation))
     id.append(item.id)
    if product_variation in existing_var_list:
     index = existing_var_list.index(product_variation)
     item_id = id[index]
     item = CartItem.objects.get(product=product, id=item_id)
     item.quantity += 1
     item.user = current_user
     item.save()
   else:
    cart_item = CartItem.objects.create(product=product, quantity=1, user=current_user)
    if len(product_variation) > 0:
     cart_item.variation.clear()
     cart_item.variation.add(*product_variation)
    cart_item.save()
  return redirect('cart')
 else:
  product_variation = []
  if request.method == 'POST':
   for item in request.POST:
    key = item
    value = request.POST[key]
    try:
     variation = ProductVariants.objects.get(product=product, variation_category__iexact=key, variation_value__iexact=value)
     product_variation.append(variation)
    except:
     pass
   try:
    cart = Cart.objects.get(cart_id=_cart_id(request))
   except Cart.DoesNotExist:
    cart = Cart.objects.create(
     cart_id=_cart_id(request)
    )
   cart.save()
   is_cart_item_exists = CartItem.objects.filter(product=product, cart=cart, variation__id__in=product_variation).exists()
   if is_cart_item_exists:
    cart_item = CartItem.objects.filter(product=product, cart=cart)
    existing_var_list = []
    id = []
    for item in cart_item:
     existing_variation = item.variation
     existing_var_list.append(list(existing_variation))
     id.append(item.id)
    if product_variation in existing_var_list:
     index = existing_var_list.index(product_variation)
     item_id = id[index]
     item = CartItem.objects.get(product=product, id=item_id)
     item.quantity += 1
     item.cart = cart
     item.save()
   else:
    cart_item = CartItem.objects.create(product=product, quantity=1, cart=cart)
    if len(product_variation) > 0:
     cart_item.variation.clear()
     cart_item.variation.add(*product_variation)
    cart_item.save()
  return redirect('cart')

def remove_cart(request, product_id, cart_item_id):
 product = get_object_or_404(Product, id=product_id)
 try:
  if request.user.is_authenticated:
   cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
  else:
   cart = Cart.objects.get(cart_id=_cart_id(request))
   cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
  if cart_item.quantity > 1:
   cart_item.quantity -= 1
   cart_item.save()
  else:
   cart_item.delete()
 except Exception:
  pass
 return redirect('cart')

def remove_cart_item(request, product_id, cart_item_id):
 product = get_object_or_404(Product, id=product_id)
 try:
  if request.user.is_authenticated:
   cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
  else:
   cart = Cart.objects.get(cart_id=_cart_id(request))
   cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
  cart_item.delete()
 except Exception:
  pass
 return redirect('cart')

@login_required(login_url='login')
def cart(request, total=0, quantity=0, cart_items=None):
 try:
  tax = 0
  grand_total = 0
  if request.user.is_authenticated:
   cart_items = CartItem.objects.filter(user=request.user, is_active=True)
  else:
   cart = Cart.objects.get(cart_id=_cart_id(request))
   cart_items = CartItem.objects.filter(cart=cart, is_active=True)
  for cart_item in cart_items:
   total += (cart_item.product.price * cart_item.quantity)
   quantity += cart_item.quantity
  tax = (2 * total) / 100
  grand_total = total + tax
 except ObjectDoesNotExist:
  pass
 context = {
  'total': total,
  'quantity': quantity,
  'cart_items': cart_items,
  'tax': tax,
  'grand_total': grand_total
 }
 return render(request, 'store/cart.html', context)

def checkout(request, total=0, quantity=0, cart_items=None):
 try:
  tax = 0
  grand_total = 0
  if request.user.is_authenticated:
   cart_items = CartItem.objects.filter(user=request.user, is_active=True)
  else:
   cart = Cart.objects.get(cart_id=_cart_id(request))
   cart_items = CartItem.objects.filter(cart=cart, is_active=True)
  for cart_item in cart_items:
   total += (cart_item.product.price * cart_item.quantity)
   quantity += cart_item.quantity
  tax = (2 * total) / 100
  grand_total = total + tax
 except ObjectDoesNotExist:
  pass
 context = {
  'total': total,
  'quantity': quantity,
  'cart_items': cart_items,
  'tax': tax,
  'grand_total': grand_total
 }
 return render(request, 'store/checkout.html', context)

def order_create(request, total=0, quantity=0, cart_items=None):
 current_user = request.user
 if current_user.is_authenticated:
  cart_items = CartItem.objects.filter(user=current_user, is_active=True)
  order_details = Order.objects.create(user=current_user, order_total=total)
  for cart_item in cart_items:
   order_product = OrderProduct()
   order_product.order_id = order_details.id
   order_product.payment = order_details.payment
   order_product.user_id = current_user.id
   order_product.product_id = cart_item.product_id
   order_product.quantity = cart_item.quantity
   order_product.product_price = cart_item.product.price
   order_product.ordered = True
   order_product.save()
   cart_item.delete()
   messages.success(request, "Your Order has been placed successfully")
   return redirect('order_complete')
 else:
  return redirect('login')