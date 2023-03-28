from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.http import HttpResponse

from accounts.models import userAddressBook as AddressBook
from saleproduct.models import ProductVariants

from .models import Cart, CartItem, Order, OrderProduct
from saleproduct.models import ProductVariants
import json
# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart

def add_cart(request): # AJAX
    if request.method == 'POST':
        user = request.user
        product_sku = request.POST.get('product_sku')
        quantity = request.POST.get('quantity',1)
        cart = Cart.objects.get_or_create(cart_id=_cart_id(request))
        if user.is_authenticated:
            is_exist = CartItem.objects.filter(
                product__sku=product_sku, user=user).exists()
            if is_exist:
                cart_item = CartItem.objects.get(
                    product__sku=product_sku, user=user)
                cart_item.quantity += int(quantity)
                cart_item.save()
            else:
                product=ProductVariants.objects.get(sku=product_sku)
                cart_item = CartItem.objects.create(
                    product=product, quantity=quantity, user=user, cart=cart[0])
                cart_item.save()
            messages.success(request, 'Product added to cart')
            context={
                'itemincart':CartItem.objects.filter(user=user).count(),
                'message':'Product added to cart',
                'code':'success'
            }
            return HttpResponse(json.dumps(context), content_type='application/json')
        else:
            messages.error(request, 'You must login to add product to cart')
            context = {
                'message': 'You must login to add product to cart',
                'code': 'error'
            }
            return  HttpResponse(json.dumps(context), content_type='application/json')
    else:
        messages.error(request, 'Method not allowed')
        context = {
            'message': 'Method not allowed',
            'code': 'error'
        }
        return HttpResponse(json.dumps(context), content_type='application/json')

def cart(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                cart=Cart.objects.get(cart_id=_cart_id(request)), user=request.user, is_active=True)
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
        'carts': cart_items,
        'tax': tax,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(ProductVariants, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id)
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except Exception:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(ProductVariants, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(
                product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(
                product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
    except Exception:
        pass
    return redirect('cart')

def update_cart(request,item_id):
    if request.method == 'POST':
        user = request.user
        product_sku = request.POST.get('product_sku')
        quantity = request.POST.get('quantity',1)
        cart = Cart.objects.get_or_create(cart_id=_cart_id(request))
        if user.is_authenticated:
            cart_item = CartItem.objects.get(
                product__sku=product_sku, user=user)
            cart_item.quantity = int(quantity)
            cart_item.save()
            context={
                'itemincart':CartItem.objects.filter(user=user).count(),
                'message':'Product added to cart',
                'code':'success'
            }
            return HttpResponse(json.dumps(context), content_type='application/json')
        else:
            messages.error(request, 'You must login to add product to cart')
            context = {
                'message': 'You must login to add product to cart',
                'code': 'error'
            }
            return  HttpResponse(json.dumps(context), content_type='application/json')
    else:
        messages.error(request, 'Method not allowed')
        context = {
            'message': 'Method not allowed',
            'code': 'error'
        }
        return HttpResponse(json.dumps(context), content_type='application/json')

@login_required(login_url='login', redirect_field_name='next')
def checkout(request, total=0, quantity=0, cart_items=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity
        tax = (2 * total) / 100
        grand_total = total + tax
        if request.user.is_authenticated:
            try:
                address = AddressBook.objects.filter(
                    user=request.user).all()
            except AddressBook.DoesNotExist:
                address = None
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'address_list': address,
    }
    return render(request, 'store/checkout.html', context)

@login_required(login_url='login', redirect_field_name='next')
def order_create(request, total=0, quantity=0, cart_items=None):
    current_user = request.user
    if current_user.is_authenticated:
        cart_items = CartItem.objects.filter(
            user=current_user, is_active=True)
        order_details = Order.objects.create(
            user=current_user, order_total=total)
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
        messages.success(
            request, "Your Order has been placed successfully")
        return redirect('order_complete')
    else:
        return redirect('login')

def order_complete(request):
    order_id = request.GET.get('order_id')
    payment_id = request.GET.get('payment_id')
    context = {
        'order_id': order_id,
        'payment_id': payment_id,
    }
    return render(request, 'store/order_complete.html', context)

def order_history(request):
    if request.user.is_authenticated:
        orders = Order.objects.filter(
            user=request.user,status=request.GET.get('status',None)).order_by('-created_at')
        context = {
            'orders': orders,
        }
        return render(request, 'store/order_history.html', context)
    else:
        return redirect('login')

def order_detail(request, order_id):
    if request.user.is_authenticated:
        order_detail = OrderProduct.objects.filter(order_id=order_id)
        order = Order.objects.get(id=order_id)
        context = {
            'order_detail': order_detail,
            'order': order,
        }
        return render(request, 'store/order_detail.html', context)
    else:
        return redirect('login')

def order_cancel(request, order_id):
    if request.get.method == 'POST':
      if request.user.is_authenticated:
          order = Order.objects.get(id=order_id)
          order.status = 'Cancelled'
          order.save()
          return redirect('order_history')
      else:
          return redirect('login')
    else:
      context={
        'status': 'Cancelled'
      }
      return redirect('order_history', context)

# here to define MOMO Payment
class PaymentView:
    def get(self, *args, **kwargs):
        return render(self.request, "store/payment.html")

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
