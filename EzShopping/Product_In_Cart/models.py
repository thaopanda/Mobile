from django.db import models
from User.models import Customer
from Product.models import Product

class Product_In_Cart(models.Model):
    customer = models.ForeignKey(Customer, related_name='customer_cart', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_cart', on_delete=models.CASCADE)
    amount = models.FloatField()
