from .models import Order, OrderItem
from django import forms

class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'user',
            'payment',
            'receiver_address',
            'order_note',
            'order_total',
        ]
        
