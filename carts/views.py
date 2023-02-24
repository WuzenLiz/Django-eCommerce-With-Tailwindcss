from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.decorators import login_required

from saleproduct.models import ProductVariants
from .models import Cart, CartItem
# Create your views here.

def _cart_id(request):
 cart = request.session.session_key
 if not cart:
  cart = request.session.create()
 return cart

@login_required(login_url='login', redirect_field_name='next')
def add_cart(request):
  if request.method == 'POST':
    product_sku = request.POST['product_sku']
    quantity = request.POST['quantity']
    product = ProductVariants.objects.get(sku=product_sku)
    try:
      cart = Cart.objects.get(cart_id=_cart_id(request))
    except Cart.DoesNotExist:
      cart = Cart.objects.create(
        cart_id=_cart_id(request)
      )
      cart.save()
    try:
      cart_item = CartItem.objects.get(product=product, cart=cart)
      if cart_item.quantity < cart_item.product.stock:
        cart_item.quantity += int(quantity)
      cart_item.save()
    except CartItem.DoesNotExist:
      cart_item = CartItem.objects.create(
        product=product,
        quantity=quantity,
        cart=cart
      )
      cart_item.save()
    return redirect(last_url(request))
  else:
    return redirect('cart')


@login_required(login_url='login', redirect_field_name='next')
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
    'grand_total': grand_total,
  }
  return render(request, 'store/cart.html', context)

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

## here to define MOMO Payment
def payment(request): 
    if request.method == 'POST':
        order_id = request.POST['order_id']
        amount = request.POST['amount']
        order = Order.objects.get(id=order_id)
        order.payment = amount
        order.save()
        url = 'https://sandbox.momodeveloper.mtn.com/collection/v1_0/requesttopay'
        headers = {
            'X-Reference-Id': str(uuid.uuid4()),
            'Ocp-Apim-Subscription-Key': '1b3f6c9d1d664a8a9a6f0c6a7d6f8f8e',
            'Content-Type': 'application/json',
            'X-Target-Environment': 'sandbox',
        }
        data = {
            'amount': amount,
            'currency': 'EUR',
            'externalId': order_id,
            'payer': {
                'partyIdType': 'MSISDN',
                'partyId': '256787665431',
            },
            'payerMessage': 'Payment for order',
            'payeeNote': 'Payment for order',
        }
        r = requests.post(url, headers=headers, data=json.dumps(data))
        print(r.json())
        return redirect('checkout')