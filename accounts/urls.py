from django.urls import path
from .views import *

# app_name = 'accounts'

urlpatterns = [
    path('', profile_view, name='profile'),
    path('dang-nhap/', login_view, name='login'),
    path('dang-xuat/', logout_view, name='logout'),
    path('dang-ky/', register_view, name='register'),
    path('dia-chi/', AddressBookView.get, name='address'),
    path('dia-chi/them-dia-chi/', AddressBookView.post, name='add_address'),
    path('dia-chi/xoa-dia-chi/<int:id>/', AddressBookView.delete, name='delete_address'),
    path('dia-chi/sua-dia-chi/<int:id>/', AddressBookView.update, name='edit_address'),
    path('dia-chi/cap-nhat-dia-chi/<int:id>/', AddressBookView.update, name='update_address'),
    path('dia-chi/thiet-lap-dia-chi/', AddressBookView.set_default, name='set_main_address'),
    # path('thay-doi-mat-khau/', change_password_view, name='change_password'),
    # path('thay-doi-mat-khau/cap-nhat-mat-khau/', update_password_view, name='update_password'),
    # path('thong-tin-ca-nhan/', profile_view, name='profile'),
    # path('thong-tin-ca-nhan/cap-nhat-thong-tin/', update_profile_view, name='update_profile'),
    # path('don-hang/', order_view, name='order'),
    # path('don-hang/<int:id>/', order_detail_view, name='order_detail'),
    path('quen-mat-khau/', forgot_password, name='forgot_password'),
]