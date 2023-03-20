from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin, AbstractBaseUser
# from cities.models import Country, City, Region, Subregion, District

# Create your models here.


class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have an username')
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUserAccount(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    date_joined = models.DateTimeField(
        verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = AccountManager()

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True

    @property
    def fullname(self):
        return self.userinfomation.full_name

    @property
    def phone(self):
        return self.userinfomation.phone

    @property
    def address(self):
        return self.userinfomation.address
    
    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class userAddressBook(models.Model):
    user = models.ForeignKey(CustomUserAccount, on_delete=models.CASCADE)
    receiver_name = models.CharField(max_length=100, blank=True, null=True)
    phone = models.CharField(max_length=100, default='')
    address = models.TextField(max_length=100)
    # region = models.ForeignKey(Region, on_delete=models.CASCADE,default='')
    # sub_region = models.ForeignKey(Subregion, on_delete=models.CASCADE,default='')
    # city = models.ForeignKey(City, on_delete=models.CASCADE,default='')
    # country = models.ForeignKey(Country, on_delete=models.CASCADE,default='')
    is_main_address = models.BooleanField(default=False)

    def __str__(self):
        return self.address

    def save(self, *args, **kwargs):
        if userAddressBook.objects.filter(user=self.user).all().count() == 0 and self.is_main_address == False:
            self.is_main_address = True
        elif userAddressBook.objects.filter(user=self.user, is_main_address=True).all().count() == 1 and self.is_main_address == True:
            userAddressBook.objects.filter(
                user=self.user, is_main_address=True).update(is_main_address=False)
        elif userAddressBook.objects.filter(user=self.user, is_main_address=True).all().count() == 0 and self.is_main_address == False:
            self.is_main_address = True
        else:
            pass
        if self.receiver_name == None:
            self.receiver_name = self.user.userinfomation.full_name
        else:
            pass
        super(userAddressBook, self).save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        if self.is_main_address == True:
            userAddressBook.objects.filter(user=self.user).exclude(
                id=self.id).update(is_main_address=True)
        else:
            pass
        super(userAddressBook, self).delete(*args, **kwargs)

    @staticmethod
    def get_user_default_address(user):
        try:
            return userAddressBook.objects.get(user=user, is_main_address=True)
        except:
            return False


class userInfomation(models.Model):
    user = models.OneToOneField(CustomUserAccount, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=100, default='')

    def __str__(self):
        return self.user.username

    @property
    def full_name(self):
        return self.last_name+' '+self.first_name

    @property
    def address(self):
        return self.user.useraddressbook.objects.filter(
            user=self.user, is_main_address=True).first().address

    def save(self, *args, **kwargs):
        if self.phone == None:
            self.phone = self.user.useraddressbook.objects.filter(
                user=self.user, is_main_address=True).first().phone
        else:
            pass
        super(userInfomation, self).save(*args, **kwargs)
