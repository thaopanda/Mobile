from django.db import models
from User.models import Customer
from Product.models import Product

class Comment(models.Model):
    customer = models.ForeignKey(Customer, related_name='customer_comment', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_comment', on_delete=models.CASCADE, null=True)
    rating = models.PositiveIntegerField(null=True)
    content = models.TextField()
    image = models.TextField(blank=True)
