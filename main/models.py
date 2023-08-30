from django.db import models

from users.models import User


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=3, decimal_places=0)
    quantity = models.PositiveIntegerField(default=0)
    image_main = models.ImageField(upload_to='products_images', default='')
    image_addition = models.ImageField(upload_to='products_images', default='')


    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name


class BagQuerySet(models.QuerySet):
    def total_sum(self):
        return sum(bag.sum() for bag in self)

    def total_quantity(self):
        return sum(bag.quantity for bag in self)


class Bag(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    product = models.ForeignKey(to=Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=0)
    created_timestamp = models.DateTimeField(auto_now_add=True)

    objects = BagQuerySet.as_manager()

    def __str__(self):
        return f'Bag for {self.user.username} | Product: {self.product.name}'

    def sum(self):
        return self.product.price * self.quantity
