from django.db import models
from User.models import Customer, Seller
from Product.models import Product
from Order.models import Order

class OrderDetailManager(models.Manager):
    def CreateOrderDetail(self, order, product, amount):
        orderDetail = self.model(product=product, order=order, amount=amount)
        orderDetail.save(using = self._db)


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, related_name='order_orderdetail', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_orderdetail', on_delete=models.CASCADE)
    amount = models.FloatField()
    objects = OrderDetailManager()

