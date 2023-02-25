from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django_filters import CharFilter, FilterSet, NumberFilter
from django_filters import rest_framework as filters
from django_filters.rest_framework import DjangoFilterBackend
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
 BannerContent = HomeBannerContent.objects.filter(is_active=True).order_by('?').first()
 Brands = Brand.objects.filter(is_active=True,is_featured=True).order_by('?')[:6]
 # get 4 new products lowest price variant
 NewProducts = Product.objects.filter(is_active=True).order_by('-created_at')[:4]
 BestSellerProducts = Product.objects.filter(is_active=True).order_by('?')[:4]
 context = {
  'BannerContent': BannerContent,
  'Brands': Brands,
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
 context = {}
 return render(request, 'saleproduct/search.html', context)

def product_detail(request, slug):
 """Product detail page."""
 product = Product.objects.get(slug=slug)
 context = {
  'product': product,
 }
 return render(request, 'saleproduct/product.html', context)

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
 context = {
  'Products': Product.objects.filter(is_active=True),
 }
 return render(request, 'saleproduct/shop.html', context)
# API views