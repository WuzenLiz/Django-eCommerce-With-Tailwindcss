from django.urls import path
from .views import *

# app_name = 'accounts'

urlpatterns = [
    path('', profile_view, name='profile'),
    path('dang-nhap/', login_view, name='login'),
    path('dang-xuat/', logout_view, name='logout'),
    path('dang-ky/', register_view, name='register'),
    path('dia-chi/', AddressBookView.get, name='address'),
    path('dia-chi/them-dia-chi/', AddressBookView.create, name='add_address'),
    path('dia-chi/xoa-dia-chi/<int:id>/', AddressBookView.delete, name='delete_address'),
    path('dia-chi/sua-dia-chi/<int:id>/', AddressBookView.update, name='edit_address'),
    path('dia-chi/cap-nhat-dia-chi/<int:id>/', AddressBookView.update, name='update_address'),
    path('dia-chi/thiet-lap-dia-chi/', AddressBookView.set_default, name='set_main_address'),
    path('quen-mat-khau/', forgot_password, name='forgot_password'),
]