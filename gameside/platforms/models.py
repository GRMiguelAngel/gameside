from django.db import models

# Create your models here.


class Platform(models.Model):
    name = models.CharField(max_length=50, unique=True)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    logo = models.ImageField(blank=True, upload_to='logos', default='logos/default.jpg')

    def __str__(self):
        return self.name
