from django.urls import path, include
from . import views

urlpatterns = [
 path('', views.cart, name='cart'),
 path('add/<int:product_id>/', views.add_cart, name='add_cart'),
 path('remove/<int:product_id>/', views.remove_cart, name='remove_cart'),
 path('remove_item/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
]