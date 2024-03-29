from django.core.paginator import Paginator
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_filters import CharFilter, FilterSet, NumberFilter
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
from hitcount.models import HitCount
from django.conf import settings
# import django hitcount
from hitcount.views import HitCountDetailView, HitCountMixin
from rest_framework import filters, generics, mixins, permissions, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser
from rest_framework.response import Response

from .model_manage import ProductManager, VariantManager
from .models import *
from .serializers import ProductSerializer


# Webviews
def index(request):
    """Shop home page."""
    BannerContent = HomeBannerContent.objects.filter(
        is_active=True).order_by('?').first()
    Brands = Brand.objects.filter(is_active=True, is_featured=True)[:6]
    Categories = Category.objects.filter(is_active=True)[:6]
    # get 4 new products lowest price variant
    NewProducts = Product.objects.filter(
        is_active=True).order_by('-created_at')[:4]
    BestSellerProducts = Product.objects.filter(
        is_active=True).order_by('?')[:4]
    context = {
        'BannerContent': BannerContent,
        'Brands': Brands,
     'Categories': Categories,
     'NewProducts': NewProducts,
     'BestSellerProducts': BestSellerProducts,
    }
    return render(request, 'saleproduct/index.html', context)


def page_not_found(request):
    """404 page."""
    context = {}
    return render(request, '404.html', context)


def server_error(request):
    """500 page."""
    context = {}
    return render(request, '500.html', context)


def search(request):
    """Search page."""
    search_query = request.GET.get('search')
    context = {
        'Products': Product.objects.filter(is_active=True, name__icontains=search_query),
        'search_query': search_query,
    }
    return render(request, 'saleproduct/shop.html', context)

# HitCount this


class ProductDetailView(HitCountDetailView):
    model = Product
    count_hit = True
    template_name = 'saleproduct/product.html'
    context_object_name = 'product'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Products'] = Product.objects.get(slug=self.kwargs['slug'])
        context['RelatedProducts'] = Product.objects.filter(is_active=True).order_by('?')[:4]
        return context

def category(request, slug,):
    """Category detail page."""
    context = {
        'Products': Product.objects.filter(category__slug=slug),
    }
    return render(request, 'saleproduct/shop.html', context)


def brand(request, slug):
    """Brand detail page."""
    context = {
        'Products': Product.objects.filter(brand__slug=slug),
    }
    return render(request, 'saleproduct/shop.html', context)


def shop(request):
    """Shop page."""
    # Products
    match request.GET.get('sort'):
        case 'price_asc':
            products = Product.objects.filter(is_active=True).order_by('variants__price')
        case 'price_desc':
            products = Product.objects.filter(is_active=True).order_by('-variants__price')
        case 'latest':
            products = Product.objects.filter(is_active=True).order_by('-created_at')
        case _:
            # get sale products
            products = Product.objects.filter(is_active=True).order_by('variants__sale_price')

    if request.GET.get('category'): # filter by category slug in url query="slug1+slug2+..."
        slugs = request.GET.get('category').split(' ')
        products = products.filter(category__slug__in=slugs)
    if request.GET.get('brand'):
        slugs = request.GET.get('brand').split(' ')
        products = products.filter(brand__slug__in=slugs)
    if request.GET.get('price'):
        prices = request.GET.get('price').split('-')
        products = products.filter(variants__price__gte=prices[0], variants__price__lte=prices[1])
    # Pagination
    paginator = Paginator(products.distinct(), settings.PAGINATE_BY)

    context = {
        'Products': paginator.get_page(request.GET.get('page')),
        'filter':{
            'category': request.GET.get('category'),
            'brand': request.GET.get('brand'),
        } 
    }
    return render(request, 'saleproduct/shop.html', context)
# API views
