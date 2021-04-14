from django.db import models
from User.models import Customer, Seller
from Product.models import Product

ORDER_STATUS = [
    ('waiting', "waiting"),
    ('denied', "denied"),
    ('accepted', "accepted"),
    ('process', "process"),
    ('shipping', "shipping"),
    ('shipped', "shipped"),
    ('refunded', "refunded"),
]


class Order(models.Model):
    seller = models.ForeignKey(Seller, related_name='seller_order', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='customer_order', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_order', on_delete=models.CASCADE)
    order_status = models.CharField(max_length=30, choices= ORDER_STATUS, blank=False, null=False)
    amount = models.FloatField()
    ship_cost = models.FloatField()

