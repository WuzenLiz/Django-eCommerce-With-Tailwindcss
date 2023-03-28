from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add', views.add_cart, name='add_cart'),
    path('update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_item/<int:product_id>/<int:cart_item_id>/',
         views.remove_cart_item, name='remove_cart_item'),
    path('checkout', views.checkout, name='checkout'),
    path('create_order', views.order_create, name='order_create'),
    path('order_complete', views.order_complete, name='order_complete'),
    # path('payment', views.payment, name='payment'),
    path('order', views.order_history, name='order'),
]
