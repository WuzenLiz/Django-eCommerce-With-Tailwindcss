import json

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render

from accounts.models import userAddressBook as AddressBook
from saleproduct.models import ProductVariants

from .forms import OrderCreateForm, PaymentForm
from .models import Cart, CartItem, Order, OrderItem, Payment_method, PayOrder, OrderProduct
from .vnpay import vnpay

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

def cart(request,cart_items=None):
    try:
        tax = 0
        grand_total = 0
        total=0
        quantity=0
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
        total_item = cart_items.count()
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'carts': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'total_item': total_item,
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
def checkout(request):
    try:
        tax = 0
        total = 0
        grand_total = 0
        quantity = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(
                user=request.user,cart=_cart_id(request) , is_active=True)
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
        'cart_id': _cart_id(request),
        'total': total,
        'cart_items': cart_items,
        'tax': tax,
        'grand_total': grand_total,
        'address_list': address,
        'payment_method': Payment_method,
    }
    return render(request, 'store/checkout.html', context)

def order_create(request):
    if request.method == 'POST':
        with transaction.atomic():
            cart_id = request.POST.get('cart_id')
            if cart_id:
                cart = Cart.objects.get(cart_id=cart_id)
            else:
                cart = Cart.objects.get(cart_id=_cart_id(request))
            address_id = request.POST.get('address_id')
            if address_id:
                address = AddressBook.objects.get(id=address_id)
            else:
                address = AddressBook.objects.filter(user=request.user).first()
            payment_method = request.POST.get('payment_method')
            user = request.user
            
            order = Order.objects.create(
                user=user,
                receiver_address=address,
                payment=payment_method,
                order_total=cart.grand_total,
                status='Order Received',
            )
            cart_items = CartItem.objects.filter(cart=cart)
            for item in cart_items:
                OrderProduct.objects.create(
                    order=order,
                    user=user,
                    product=item.product,
                    quantity=item.quantity,
                    product_price=item.product.price,
                    ordered=True,
                )
            CartItem.objects.filter(cart=cart).delete()
            context = {
                'order_code': order.id,
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

# VNPay Payment
def payment(request):

    if request.method == 'POST':
        # Process input data and build url payment
        form = PaymentForm(request.POST)
        if form.is_valid():
            order_type = form.cleaned_data['order_type']
            order_id = form.cleaned_data['order_id']
            amount = form.cleaned_data['amount']
            order_desc = form.cleaned_data['order_desc']
            bank_code = form.cleaned_data['bank_code']
            language = form.cleaned_data['language']
            ipaddr = get_client_ip(request)
            # Build URL Payment
            vnp = vnpay()
            vnp.requestData['vnp_Version'] = '2.1.0'
            vnp.requestData['vnp_Command'] = 'pay'
            vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
            vnp.requestData['vnp_Amount'] = amount * 100
            vnp.requestData['vnp_CurrCode'] = 'VND'
            vnp.requestData['vnp_TxnRef'] = order_id
            vnp.requestData['vnp_OrderInfo'] = order_desc
            vnp.requestData['vnp_OrderType'] = order_type
            # Check language, default: vn
            if language and language != '':
                vnp.requestData['vnp_Locale'] = language
            else:
                vnp.requestData['vnp_Locale'] = 'vn'
                # Check bank_code, if bank_code is empty, customer will be selected bank on VNPAY
            if bank_code and bank_code != "":
                vnp.requestData['vnp_BankCode'] = bank_code

            vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
            vnp.requestData['vnp_IpAddr'] = ipaddr
            vnp.requestData['vnp_ReturnUrl'] = settings.VNPAY_RETURN_URL
            vnpay_payment_url = vnp.get_payment_url(settings.VNPAY_PAYMENT_URL, settings.VNPAY_HASH_SECRET_KEY)
            return redirect(vnpay_payment_url)
        else:
            print("Form input not validate")
    else:
        return render(request, "vnpay/payment.html", {"title": "Thanh toán"})

def payment_ipn(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = inputData['vnp_Amount']
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            # Check & Update Order Status in your Database
            # Your code here
            firstTimeUpdate = True
            totalamount = True
            if totalamount:
                if firstTimeUpdate:
                    if vnp_ResponseCode == '00':
                        print('Payment Success. Your code implement here')
                    else:
                        print('Payment Error. Your code implement here')

                    # Return VNPAY: Merchant update success
                    result = JsonResponse({'RspCode': '00', 'Message': 'Confirm Success'})
                else:
                    # Already Update
                    result = JsonResponse({'RspCode': '02', 'Message': 'Order Already Update'})
            else:
                # invalid amount
                result = JsonResponse({'RspCode': '04', 'Message': 'invalid amount'})
        else:
            # Invalid Signature
            result = JsonResponse({'RspCode': '97', 'Message': 'Invalid Signature'})
    else:
        result = JsonResponse({'RspCode': '99', 'Message': 'Invalid request'})

    return result

def payment_return(request):
    inputData = request.GET
    if inputData:
        vnp = vnpay()
        vnp.responseData = inputData.dict()
        order_id = inputData['vnp_TxnRef']
        amount = int(inputData['vnp_Amount']) / 100
        order_desc = inputData['vnp_OrderInfo']
        vnp_TransactionNo = inputData['vnp_TransactionNo']
        vnp_ResponseCode = inputData['vnp_ResponseCode']
        vnp_TmnCode = inputData['vnp_TmnCode']
        vnp_PayDate = inputData['vnp_PayDate']
        vnp_BankCode = inputData['vnp_BankCode']
        vnp_CardType = inputData['vnp_CardType']
        if vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY):
            if vnp_ResponseCode == "00":
                return render(request, "payment_return.html", {"title": "Kết quả thanh toán",
                                                               "result": "Thành công", "order_id": order_id,
                                                               "amount": amount,
                                                               "order_desc": order_desc,
                                                               "vnp_TransactionNo": vnp_TransactionNo,
                                                               "vnp_ResponseCode": vnp_ResponseCode})
            else:
                return render(request, "payment_return.html", {"title": "Kết quả thanh toán",
                                                               "result": "Lỗi", "order_id": order_id,
                                                               "amount": amount,
                                                               "order_desc": order_desc,
                                                               "vnp_TransactionNo": vnp_TransactionNo,
                                                               "vnp_ResponseCode": vnp_ResponseCode})
        else:
            return render(request, "payment_return.html",
                          {"title": "Kết quả thanh toán", "result": "Lỗi", "order_id": order_id, "amount": amount,
                           "order_desc": order_desc, "vnp_TransactionNo": vnp_TransactionNo,
                           "vnp_ResponseCode": vnp_ResponseCode, "msg": "Sai checksum"})
    else:
        return render(request, "vnpay/payment_return.html", {"title": "Kết quả thanh toán", "result": ""})


def query(request):
    if request.method == 'GET':
        return render(request, "vnpay/query.html", {"title": "Kiểm tra kết quả giao dịch"})
    else:
        # Add paramter
        vnp = vnpay()
        vnp.requestData = {}
        vnp.requestData['vnp_Command'] = 'querydr'
        vnp.requestData['vnp_Version'] = '2.1.0'
        vnp.requestData['vnp_TmnCode'] = settings.VNPAY_TMN_CODE
        vnp.requestData['vnp_TxnRef'] = request.POST['order_id']
        vnp.requestData['vnp_OrderInfo'] = 'Kiem tra ket qua GD OrderId:' + request.POST['order_id']
        vnp.requestData['vnp_TransDate'] = request.POST['trans_date']  # 20150410063022
        vnp.requestData['vnp_CreateDate'] = datetime.now().strftime('%Y%m%d%H%M%S')  # 20150410063022
        vnp.requestData['vnp_IpAddr'] = get_client_ip(request)
        requestUrl = vnp.get_payment_url(settings.VNPAY_API_URL, settings.VNPAY_HASH_SECRET_KEY)
        responseData = urllib.request.urlopen(requestUrl).read().decode()
        print('RequestURL:' + requestUrl)
        print('VNPAY Response:' + responseData)
        data = responseData.split('&')
        for x in data:
            tmp = x.split('=')
            if len(tmp) == 2:
                vnp.responseData[tmp[0]] = urllib.parse.unquote(tmp[1]).replace('+', ' ')

        print('Validate data from VNPAY:' + str(vnp.validate_response(settings.VNPAY_HASH_SECRET_KEY)))
        return render(request, "vnpay/query.html", {"title": "Kiểm tra kết quả giao dịch", "data": vnp.responseData})


def refund(request):
    return render(request, "vnpay/refund.html", {"title": "Gửi yêu cầu hoàn tiền"})


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip

