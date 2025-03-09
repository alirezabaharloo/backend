from django.db import models
from accounts.models import Shop

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=250)
    parent_cat = models.ForeignKey('self', related_name='children', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"


class Product(models.Model):
    # relational fields
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE, related_name='products')
    category = models.ManyToManyField(Category, related_name='products')

    # info fields
    title = models.CharField(max_length=250, null=True, db_index=True)
    body = models.TextField(null=True)
    image = models.ImageField(default='products/', null=True)

    # cost fields
    quantity = models.PositiveIntegerField(default=0)
    price = models.PositiveIntegerField(null=True)
    discount = models.PositiveIntegerField(blank=True, null=True)


    @property
    def calc_cost(self):
        return self.price - (self.price * (self.discount / 100)) if self.discount else self.price


    def __str__(self):
        return f'{self.title} - {self.shop}'