from django.db import models
from User.models import Customer
from Product.models import Product

class Rating(models.Model):
    customer = models.ForeignKey(Customer, related_name='customer_rating', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_rating', on_delete=models.CASCADE, null=True)
    rating = models.PositiveIntegerField()
