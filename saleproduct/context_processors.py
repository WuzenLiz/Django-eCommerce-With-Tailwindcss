from .models import Category, Brand
from carts.models import CartItem, Cart
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

    if request.session.session_key is None:
        request.session.save()
    itemincart = CartItem.objects.filter(
        cart=Cart.objects.get_or_create(cart_id=request.session.session_key)[0]
    ).count()

    categories, brands = None, None
    product_search_query = request.GET.get('search')

    # if there is no search query, list all categories and brands
    if not product_search_query:
        categories = Category.objects.filter(is_active=True).only('name', 'slug', 'category_icon')
        brands = Brand.objects.filter(is_active=True).only('name', 'slug', 'brand_image')
    else:
        categories = Category.objects.filter(
            is_active=True, name__icontains=product_search_query
        ).only('name', 'slug', 'category_icon')
        brands = Brand.objects.filter(
            is_active=True, name__icontains=product_search_query
        ).only('name', 'slug', 'brand_image')

    context = {
        'search_query': product_search_query,
        'categories': categories,
        'brands': brands,
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