from django.http import HttpRequest, HttpResponse

from shared.decorators import correct_method, game_exists

from users.views import auth
from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer

# Create your views here.


@correct_method('GET')
def game_list(request: HttpRequest) -> HttpResponse:
    games = Game.objects.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@correct_method('GET')
@game_exists
def game_detail(request: HttpRequest, game_slug: str) -> HttpResponse:
    game = Game.objects.get(slug=game_slug)
    serializer = GameSerializer(game, request=request)
    return serializer.json_response()


# def game_filter(request: HttpRequest, *categories: str) -> HttpRequest


@correct_method('GET')
def game_reviews(request: HttpRequest, game_slug: str) -> HttpResponse:
    game = Game.objects.get(slug=game_slug)
    reviews = Review.objects.filter(game=game)
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()


@correct_method('POST')
def add_review(request: HttpRequest, game_slug: str) -> HttpResponse:
    token = request.headers.get('Authoritation')
    pass


@correct_method('GET')
def review_detail(request: HttpRequest, review_pk: int) -> HttpResponse:
    review = Review.objects.get(pk=review_pk)
    serializer = ReviewSerializer(review, request=request)
    return serializer.json_response()
