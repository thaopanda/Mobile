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

class OrderManager(models.Manager):
    def CreateOrder(self, seller, customer, order_status, ship_cost):
        order = self.model(seller=seller, customer=customer, order_status=order_status, ship_cost=ship_cost)
        order.save(using = self._db)
        return order

class Order(models.Model):
    seller = models.ForeignKey(Seller, related_name='seller_order', on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, related_name='customer_order', on_delete=models.CASCADE)

    order_status = models.CharField(max_length=30, choices= ORDER_STATUS, blank=False, null=False)
    ship_cost = models.FloatField()
    product_cost = models.FloatField(null=True)
    objects = OrderManager()

