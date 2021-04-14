from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser


USER_TYPE = [
    ('customer', "customer"),
    ('seller', "seller"),
    ('admin', "admin"),
]

GENDER = [
    ('male', 'male'),
    ('female', 'female'),
    ('other', 'other'),
    ('', '')
]

SHOP = [
    ("Thời trang", "Thời trang"),
    ("Công nghệ", "Công nghệ"),
    ("Trang trí", "Trang trí"),
    ("Sức khỏe và Sắc đẹp", "Sức khỏe và Sắc đẹp"),
    ("Nhà cửa và đời sống", "Nhà cửa và đời sống"),
    ("Mẹ và bé", "Mẹ và bé"),
    ("Nhà sách online", "Nhà sách online"),
    ("Ô tô - xe máy", "Ô tô - xe máy"),
    ("Thể thao du lịch", "Thể thao du lịch"),
    ("Khác", "Khác")
]

class UserManager(BaseUserManager):
 
    def get_by_natural_key(self, email):
        return self.get(email=email)

    def create_superuser(self, email, username, password):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.set_password(password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.user_type='admin'
        user.save(using = self._db)
        return user
 
class CustomerManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.user_type = "customer"
        user.set_password(password)
        user.save(using=self._db)
        return user

class AdminManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('User must have an email address')
        if not username:
            raise ValueError('User must have a username')
        user = self.model(
            email = self.normalize_email(email),
            username = username,
        )
        user.user_type = "admin"
        user.set_password(password)
        user.save(using=self._db)
        return user

class SellerManager(BaseUserManager):
    def create_user(self, email, username, fullname, identication, address, phoneNumber, shopName, shopCategory, password=None):
        if not email:
            raise ValueError('Seller must have an email address')
        if not username:
            raise ValueError('Seller must have a username')
        if not fullname:
            raise ValueError('Seller must have fullname')
        if not identication:
            raise ValueError('Seller must have identication')
        if not address:
            raise ValueError('Seller mus have address')
        if not phoneNumber:
            raise ValueError('Seller must have phoneNumber')

        user = self.model(
            email = self.normalize_email(email),
            username = username,
            fullname = fullname,
            identication = identication,
            address = address,
            phoneNumber = phoneNumber,
            shopName = shopName,
            shopCategory = shopCategory
        )
        user.user_type = "seller"
        user.has_update_permission = False
        user.set_password(password)
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    user_type = models.CharField(choices=USER_TYPE, null=False, blank=False, max_length=10)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    # last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    email = models.EmailField(verbose_name='email', max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True)
    image = models.TextField(blank=True)

    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.email
    
    def has_module_perms(self, app_label):
        return True
    
    def has_perm(self, perm, obj=None):
        return self.is_admin

class Seller(MyUser):
    fullname = models.CharField(max_length=50, unique=False)
    identication = models.CharField(max_length=20, unique=True)
    address = models.CharField(max_length=100)
    phoneNumber = models.CharField(max_length=20, unique=True)
    shopName = models.CharField(max_length=100, unique=False, default='')
    shopCategory = models.CharField(max_length=100, unique=False, default='')
    followed = models.PositiveIntegerField(default=0)


    # is_confirmed = models.BooleanField(default=False)
    # has_update_permission = models.BooleanField(default=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'fullname', 'identication', 'address', 'phoneNumber']

    objects = SellerManager()

    def __str__(self):
        return self.username


class Customer(MyUser):
    fullname = models.CharField(max_length=50, unique=False, blank=True, null=True)
    gender = models.CharField(max_length=10, choices=GENDER, blank=True, null=True)
    phone = models.CharField(max_length=10, blank=True, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    def __str__(self):
        return self.username

    objects = CustomerManager()

class Admin(MyUser):
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = AdminManager()




