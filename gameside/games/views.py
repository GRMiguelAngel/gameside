import json
import re

from django.http import HttpRequest, HttpResponse, JsonResponse

from shared.decorators import correct_method, game_exists, required_fields, review_exists

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
@game_exists
def game_reviews(request: HttpRequest, game_slug: str) -> HttpResponse:
    game = Game.objects.get(slug=game_slug)
    reviews = Review.objects.filter(game=game)
    serializer = ReviewSerializer(reviews, request=request)
    return serializer.json_response()

@correct_method('POST')
@required_fields('rating', 'comment')
@game_exists
def add_review(request: HttpRequest, game_slug: str) -> HttpResponse:
    payload = request.headers.get('Authorization')
    json_body = json.loads(request.body)
    rating, comment = json_body['rating'], json_body['comment']
    valid_token = r'^Bearer (?P<token>[0-9a-f]1{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12})$'
    if not (regexp := re.fullmatch(valid_token, payload)):
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)

    # Review.objects.create()

    pass


@correct_method('GET')
@review_exists
def review_detail(request: HttpRequest, review_pk: int) -> HttpResponse:
    review = Review.objects.get(pk=review_pk)
    serializer = ReviewSerializer(review, request=request)
    return serializer.json_response()
