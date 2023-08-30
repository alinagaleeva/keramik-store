from datetime import datetime

from django.db import models

from main.models import Bag
from users.models import User


class Order(models.Model):
    CREATED = 0
    PAID = 1
    ON_WAY = 2
    DELIVERED = 3
    STATUSES = (
        (CREATED, 'created'),
        (PAID, 'paid'),
        (ON_WAY, 'on way'),
        (DELIVERED, 'delivered'),
    )

    first_name = models.CharField(max_length=64)
    last_name = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    city = models.CharField(max_length=64)
    postal_code = models.BigIntegerField()
    address = models.CharField(max_length=256)
    phone = models.BigIntegerField()
    basket_history = models.JSONField(default=dict)
    created = models.DateTimeField(auto_now_add=True)
    status = models.SmallIntegerField(default=CREATED, choices=STATUSES)
    initiator = models.ForeignKey(to=User, on_delete=models.CASCADE)

    def __str__(self):
        return f'Order # {self.id}. {self.first_name} {self.last_name}'

    def update_after_payment(self):
        bags = Bag.objects.filter(user=self.initiator)
        self.status = self.PAID
        self.basket_history = {
            'order_date':
                datetime(
                    self.created.year, self.created.month, self.created.day, self.created.hour, self.created.minute
                ).strftime('%d.%m.%y %H:%M'),
            'total_price': str(bags.total_sum()),
        }
        bags.delete()
        self.save()
