from django.urls import path
from .views import *

#Urls define
urlpatterns = [
    path('', index, name='index'),
    path('shop/', shop, name='shop'),
    path('category/<slug:slug>/', category, name='category'),
    path('category/<slug:slug>/<slug:sub_slug>/', category, name='category'),
    path('product/<slug:slug>/', ProductDetailView.as_view(), name='product_detail'),
    path('brand/<slug:slug>/', brand, name='brand'),
    path('404/', page_not_found, name='page_not_found'),
    path('500/', server_error, name='server_error'),
    path('search/', search, name='search'),
]