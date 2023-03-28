from django.urls import path, include
from . import views

vnpaypatterns = [
    path('payment/', views.payment, name='payment'),
    path('payment_ipn/', views.payment_ipn, name='payment_ipn'),
    path('payment_return/', views.payment_return, name='payment_return'),
    path('query/', views.query, name='query'),
    path('refund/', views.refund, name='refund'),
]

urlpatterns = [
    path('', views.cart, name='cart'),
    path('add', views.add_cart, name='add_cart'),
    path('update/<int:item_id>/', views.update_cart, name='update_cart'),
    path('remove/<int:product_id>/', views.remove_cart, name='remove_cart'),
    path('remove_item/<int:product_id>/<int:cart_item_id>/',
         views.remove_cart_item, name='remove_cart_item'),
    path('checkout', views.checkout, name='checkout'),
    path('create_order', views.order_create, name='order_create'),
    path('order', views.order_history, name='order'),

    #VNPAY 
    path('vnpay/', include(vnpaypatterns)),
]

