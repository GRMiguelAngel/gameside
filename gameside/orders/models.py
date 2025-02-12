from django.conf import settings
from django.db import models
import uuid 


# Create your models here.
class Order(models.Model):
    class Status(models.IntegerChoices):
        INITIATED = 1
        CONFIRMED = 2
        PAID = 3
        CANCELLED = -1

    status = models.IntegerField(choices=Status, default=Status.INITIATED)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    key = models.UUIDField(unique=True, default=uuid.uuid4)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders'
    )
    games = models.ManyToManyField('games.Game', related_name='orders', blank=True)

    @property
    def price(self):
        price = 0
        for game in self.games.all():
            price += game.price
        return price

    def __str__(self):
        return f'{self.user} - {self.games}'
