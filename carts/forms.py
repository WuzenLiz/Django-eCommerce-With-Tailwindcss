from .models import Order, OrderItem
from django import forms

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            'user',
            'payment',
            'receiver_address',
            'order_note',
            'order_total',
        ]
        
class PaymentForm(forms.Form):

    order_id = forms.CharField(max_length=250)
    order_type = forms.CharField(max_length=20)
    amount = forms.IntegerField()
    order_desc = forms.CharField(max_length=100)
    bank_code = forms.CharField(max_length=20, required=False)
    language = forms.CharField(max_length=2)