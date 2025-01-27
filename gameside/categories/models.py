from colorfield.fields import ColorField
from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    color = ColorField(blank=True)

    def __str__(self):
        return self.name
