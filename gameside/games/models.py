from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# Create your models here.


class Game(models.Model):
    class Pegi(models.IntegerChoices):
        PEGI3 = 3
        PEGI7 = 7
        PEGI12 = 12
        PEGI16 = 16
        PEGI18 = 18

    pegi = models.IntegerField(choices=Pegi)

    title = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(blank=True, upload_to='covers', default='covers/default.jpg')
    price = models.DecimalField(max_digits=5, decimal_places=2)
    stock = models.IntegerField()
    released_at = models.DateField()
    category = models.ForeignKey(
        'categories.Category',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='games_category',
    )
    platforms = models.ManyToManyField('platforms.Platform', related_name='games')

    def __str__(self):
        return self.title


class Review(models.Model):
    comment = models.TextField()
    rating = models.PositiveSmallIntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    game = models.ForeignKey('Game', on_delete=models.CASCADE, related_name='reviews')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reviews'
    )

    def __str__(self):
        return self.comment
