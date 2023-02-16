from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _

# Create Auth views 
def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request=request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                messages.error(request, _("Invalid username or password."))
        else:
            messages.error(request, _("Invalid username or password."))
    form = AuthenticationForm()
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

def profile_view(request):
    return render(
        request=request,
        template_name="accounts/profile.html",
    )