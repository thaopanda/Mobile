from django.db import models
from User.models import Seller


PRODUCT_CLASS = [
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

class Product(models.Model):
    product_name = models.TextField()
    price = models.PositiveIntegerField()
    description = models.TextField()
    unit = models.CharField(max_length=30, blank=False, default="item")
    in_stock = models.PositiveIntegerField(default=0)
    status = models.CharField(max_length=30, blank=False, default="Sold out")

    product_class = models.CharField(max_length=30, blank=True, null = True)

    seller = models.ForeignKey(Seller, related_name='product_seller', on_delete=models.CASCADE, null=True)
    vendor = models.CharField(max_length=100, default='No brand')
    
    total_views = models.PositiveIntegerField(default=0)
    
    total_like = models.PositiveIntegerField(default=0)

    commentNum = models.PositiveIntegerField(default=0)

    averageRate = models.FloatField(default=0.0)
    
    sold = models.PositiveIntegerField(default=0)

# id int [pk, increment]
#   product_name varchar [not null]
#   price int [not null]
#   unit varchar [not null]
#   seller_id int [not null]
#   description varchar [not null]
#   in_stock int [not null]
#   status varchar
#   product_class int
#   volume float8 [not null]
#   weight float8 [not null]