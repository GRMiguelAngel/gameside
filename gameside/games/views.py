from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from platforms.models import Platform
from .serializers import GameSerializer

from .forms import AddReviewForm
from .models import Game, Review

# Create your views here.



def game_list(request: HttpRequest) -> HttpResponse:
    games = Game.objects.all()
    serializer = GameSerializer(games)
    return serializer.json_response()

def game_detail(request: HttpRequest, game_slug: str) -> HttpResponse:
    game = Game.objects.get(slug=game_slug)
    platforms = Platform.objects.filter(games=game)
    return render(request, 'games/game_detail.html', dict(game=game, platforms=platforms))


# def game_filter(request: HttpRequest, *categories: str) -> HttpRequest


def game_reviews(request: HttpRequest, game_slug: str) -> HttpResponse:
    game = Game.objects.get(slug=game_slug)
    reviews = Review.objects.filter(game=game)
    return render(request, 'games/game_detail.html', dict(reviews=reviews))


def add_review(request: HttpRequest, game_slug: str) -> HttpResponse:
    if request.method == 'POST':
        if (form := AddReviewForm(request.POST)).is_valid():
            form.save()
            return redirect('games:game-list')
    else:
        form = AddReviewForm()
    return render(request, 'games/game_detail.html', dict(form=form))
