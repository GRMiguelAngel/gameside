from django.http import HttpRequest, HttpResponse

from shared.decorators import correct_method, game_exists

from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer

# Create your views here.


@correct_method
def game_list(request: HttpRequest) -> HttpResponse:
    games = Game.objects.all()
    serializer = GameSerializer(games, request=request)
    return serializer.json_response()


@correct_method
@game_exists
def game_detail(request: HttpRequest, game_slug: str) -> HttpResponse:
    game = Game.objects.get(slug=game_slug)
    serializer = GameSerializer(game, request=request)
    return serializer.json_response()


# def game_filter(request: HttpRequest, *categories: str) -> HttpRequest


@correct_method
def game_reviews(request: HttpRequest, game_slug: str) -> HttpResponse:
    game = Game.objects.get(slug=game_slug)
    reviews = Review.objects.filter(game=game)
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()


def add_review(request: HttpRequest, game_slug: str) -> HttpResponse:
    token = request.headers.get('Authoritation')
    print(request.headers)
    pass


@correct_method
def review_detail(request: HttpRequest, review_pk: int) -> HttpResponse:
    review = Review.objects.get(pk=review_pk)
    serializer = ReviewSerializer(review, request=request)
    return serializer.json_response()
