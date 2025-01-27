from django.contrib import admin

from .models import Game, Review


# Register your models here.
@admin.register(Game)
class GameAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'stock']


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['game', 'rating']
