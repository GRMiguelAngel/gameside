from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render

from .forms import AddReviewForm
from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer

# Create your views here.


def game_list(request: HttpRequest) -> HttpResponse:
    games = Game.objects.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


def game_detail(request: HttpRequest, game_slug: str) -> HttpResponse:
    game = Game.objects.get(slug=game_slug)
    serializer = GameSerializer(game, request=request)
    return serializer.json_response()


# def game_filter(request: HttpRequest, *categories: str) -> HttpRequest


def game_reviews(request: HttpRequest, game_slug: str) -> HttpResponse:
    game = Game.objects.get(slug=game_slug)
    reviews = Review.objects.filter(game=game)
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()


def add_review(request: HttpRequest, game_slug: str) -> HttpResponse:
    if request.method == 'POST':
        if (form := AddReviewForm(request.POST)).is_valid():
            form.save()
            return redirect('games:game-list')
    else:
        form = AddReviewForm()
    return render(request, 'games/game_detail.html', dict(form=form))


def review_detail(request: HttpRequest, review_pk: int) -> HttpResponse:
    review = Review.objects.get(pk=review_pk)
    serializer = ReviewSerializer(review, request=request)
    return serializer.json_response()
