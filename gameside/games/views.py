from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from platforms.models import Platform

from .models import Game, Review

# Create your views here.


def game_list(request: HttpRequest) -> HttpResponse:
    games = Game.objects.all()
    return render(request, 'games/games_list.html', dict(games=games))


def game_detail(request: HttpRequest, game_slug: str) -> HttpResponse:
    game = Game.objects.get(slug=game_slug)
    platforms = Platform.objects.filter(games=game)
    return render(request, 'games/game_detail.html', dict(game=game, platforms=platforms))


# def game_filter(request: HttpRequest, *categories: str) -> HttpRequest


def game_reviews(request: HttpRequest, game_slug: str) -> HttpResponse:
    game = Game.objects.get(slug=game_slug)
    reviews = Review.objects.filter(game=game)
    return render(request, 'games/game_detail.html', dict(reviews=reviews))
