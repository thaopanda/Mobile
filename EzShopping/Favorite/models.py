from django.db import models
from User.models import Customer
from Product.models import Product


class FavoriteManager(models.Manager):
    def createFavorite(self, customer, product):
        favo = self.model(customer=customer, product=product)
        favo.save(using = self._db)
        return(favo)
class Favorite(models.Model):
    customer = models.ForeignKey(Customer, related_name='customer_favorite', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='product_favorite', on_delete=models.CASCADE, null=True)
    objects = FavoriteManager()
