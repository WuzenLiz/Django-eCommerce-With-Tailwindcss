from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import get_user_model
from .models import *

User = get_user_model()

class UserInformationInline(admin.StackedInline):
 model = userInfomation
 can_delete = False
 verbose_name_plural = 'User Information' 
 fk_name = 'user'

class UserAddressBookInline(admin.StackedInline):
 model = userAddressBook
 can_delete = False
 verbose_name_plural = 'User Address Book' 
 fk_name = 'user'
 extra = 0


class AccountAdmin(UserAdmin):
 list_display = ('email', 'username', 'is_staff', 'is_active', 'date_joined')
 list_display_links = ('email', 'username')
 readonly_fields = ('date_joined', 'last_login')
 ordering = ('-date_joined',)
 filter_horizontal = ()
 list_filter = ()
 fieldsets = ()
 add_fieldsets = (
  (None, {
   'classes': ('wide',),
   'fields': ('email', 'username', 'password1', 'password2', 'is_staff', 'is_active')}
  ),
 )
 search_fields = ('email', 'username')
 inlines = (UserInformationInline, UserAddressBookInline)

 def get_fieldsets(self, request, obj=None):
  if not obj:
   return self.add_fieldsets
  return super(AccountAdmin, self).get_fieldsets(request, obj)

 def get_queryset(self, request):
  qs = super(AccountAdmin, self).get_queryset(request)
  if request.user.is_superuser:
   return qs
  return qs.filter(is_superuser=False)
 
admin.site.register(CustomUserAccount, AccountAdmin)