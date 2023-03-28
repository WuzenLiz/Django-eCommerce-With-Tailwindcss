from .models import userAddressBook as AddressBook
from django import forms

class AddressForm(forms.ModelForm):
    class Meta:
        model = AddressBook
        fields = ['receiver_name','phone','address','is_main_address']
        widgets = {
            'receiver_name': forms.TextInput(attrs={'class': 'input input-bordered w-full mt-2'}),
            'phone': forms.TextInput(attrs={'class': 'input input-bordered w-full mt-2'}),
            'address': forms.Textarea(attrs={'class': 'input input-bordered w-full mt-2'}),
            'is_main_address': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class PasswordResetForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control'}),
    )