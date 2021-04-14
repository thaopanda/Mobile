from django.contrib import admin
from User.models import MyUser, Customer, Seller

admin.site.register(MyUser)
admin.site.register(Customer)
admin.site.register(Seller)
# Register your models here.
