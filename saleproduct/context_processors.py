from .models import Category,Brand
from carts.models import Cart
from django.conf import settings

def get_info(request):
    sitename = settings.SITE_NAME
    shopname = settings.SHOP_NAME
    shopaddress = settings.SHOP_ADDRESS
    shopphone = settings.SHOP_PHONE
    shopemail = settings.SHOP_EMAIL
    shopfacebook = settings.SHOP_FACEBOOK
    shopinstagram = settings.SHOP_INSTAGRAM
    shopzalo = settings.SHOP_ZALO
    shoptiktok = settings.SHOP_TIKTOK
    itemincart = Cart.objects.filter(cart_id=request.session.get('cart_id',0)).count()

    context = {
        'categories': Category.objects.filter(is_active=True).all(),
        'brands': Brand.objects.filter(is_active=True).all(),
        'sitename': sitename,
        'shopname': shopname,
        'shopaddress': shopaddress,
        'shopphone': shopphone,
        'shopemail': shopemail,
        'shopfacebook': shopfacebook,
        'shopinstagram': shopinstagram,
        'shopzalo': shopzalo,
        'shoptiktok': shoptiktok,
        'itemincart': itemincart,
    }
    return context