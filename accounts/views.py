from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import DetailView, ListView
from django.views.generic.edit import FormMixin
from django.conf import settings as sett
from django.http import JsonResponse

from carts.models import Cart, Order

from .forms import AddressForm, PasswordResetForm
from .models import userAddressBook as AddressBook


# Create Auth views 
def login_view(request,next=None):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                if next:
                    return redirect(next)
                return redirect("index")
            else:
                messages = messages.error(
                    request,
                    _("Invalid username or password."),
                )
                return redirect("login", next=next,messages=messages)
    form = AuthenticationForm()
    if next:
        messages.info(request, _("You must be logged in to access this page."))
    return render(
        request=request,
        template_name="accounts/login.html",
        context={"form": form},
    )

def logout_view(request):
    logout(request)
    messages.info(request, "Logged out successfully!")
    return redirect("index")

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("index")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = UserCreationForm
    return render(
        request=request,
        template_name="accounts/register.html",
        context={"register_form": form},
    )

def forgot_password(request):
    if request.method == "POST":
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            form.save(
                request=request,
                from_email=sett.EMAIL_MASTER,
                subject_template_name="accounts/password_reset_subject.txt",
                email_template_name="accounts/password_reset_email.html",
            )
            messages.success(request, "Password reset email has been sent.")
            return redirect("login")
    return render(
        request=request,
        template_name="accounts/forgot.html",
    )


def profile_view(request):
    address = AddressBook.objects.filter(user=request.user, is_main_address=True).first()
    bought_total = Order.objects.filter(user=request.user).count()
    Total_cost = Order.objects.filter(user=request.user).aggregate(total=Sum('order_total'))
    context = {
        'user': request.user,
        "address": address,
        "bought_total": bought_total,
        "Total_cost": Total_cost,
    }
    return render(
        request=request,
        template_name="accounts/profile/profile.html",
        context=context,
    )


class AddressBookView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form = AddressForm()
        user = self.user
        context = {
            'form': form,
            'address': AddressBook.objects.filter(user=user).exclude(is_main_address=True),
            'main_address': AddressBook.objects.filter(user=user, is_main_address=True).first(),
        }
        return render(self, 'accounts/profile/address.html', context)

    def create(self, *args, **kwargs):
        form = AddressForm(self.POST)
        user = self.user
        if form.is_valid():
            address = form.save(commit=False)
            address.user = user
            address.save()
            messages.success(self, "Address added successfully")
            return redirect('address')
        messages.error(self, "Address added failed")
        return render(request, 'accounts/profile/address.html', {'form': form})

    def delete(self, *args, **kwargs):
        id = kwargs.get('id')
        if id:
            address = AddressBook.objects.get(id=id)
            address.delete()
            messages.success(self, "Address deleted successfully")
            return redirect(to='address')
        messages.error(self, "Address deleted failed! No id found")
        return redirect(to='address')
        
    
    def set_default(self, *args, **kwargs):
        id = kwargs.get('id')
        if id:
            address = AddressBook.objects.get(id=id)
            address.is_main_address = True
            address.save()
            messages.success(self, "Address set as default")
            return redirect(to='address')
        messages.error(self, "Address set as default failed! No id found")
        return redirect(to='address')

    def update(self, *args, **kwargs):
        id = kwargs.get('id')
        if id:
            address = AddressBook.objects.get(id=id)
            form = AddressForm(self.POST, instance=address)
            if form.is_valid():
                form.save()
                messages.success(self, "Address updated successfully")
                return redirect(to='address')
            messages.error(self, "Address updated failed")
            redirect(to='address')
        messages.error(self, "Address updated failed! No id found")
        return redirect(to='address')