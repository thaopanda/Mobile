from django.db import models
from Product.models import Product


class ProductImageManager(models.Manager):
    def CreateProductImage(self, product, image, priority):
        productImage = self.model(product=product, image=image, priority=priority)
        productImage.save(using = self._db)

class ProductImage(models.Model):
    product = models.ForeignKey(Product, related_name='product_productImage', on_delete=models.CASCADE)
    image = models.TextField()
    priority = models.PositiveIntegerField(default=0)
    objects = ProductImageManager()