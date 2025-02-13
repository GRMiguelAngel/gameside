import json
import re

from django.http import HttpRequest, HttpResponse, JsonResponse

from shared.decorators import (
    correct_method,
    game_exists,
    required_fields,
    review_exists,
    token_check,
)
from users.models import Token

from .models import Game, Review
from .serializers import GameSerializer, ReviewSerializer

# Create your views here.


@correct_method('GET')
def game_list(request: HttpRequest) -> HttpResponse:
    category_filter = request.GET.get('category')
    platform_filter = request.GET.get('platform')

    games = Game.objects.all()

    if category_filter:
        games = games.filter(category__slug=category_filter)

    elif platform_filter:
        games = games.filter(platforms__slug=platform_filter)

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
@token_check

@game_exists
def add_review(request: HttpRequest, game_slug: str) -> HttpResponse:
    json_body = json.loads(request.body)
    payload = request.headers.get('Authorization')
    rating, comment = json_body['rating'], json_body['comment']
    if rating > 5 or rating < 1:
        return JsonResponse({'error': 'Rating is out of range'}, status=400)
    regexp = r'Bearer\s(?P<token>[\d|a-f]{8}-[\d|a-f]{4}-[\d|a-f]{4}-[\d|a-f]{4}-[\d|a-f]{12})'
    captured_token = re.fullmatch(regexp, payload)['token']
    token = Token.objects.get(key=captured_token)
    game = Game.objects.get(slug=game_slug)
    review = Review.objects.create(rating=rating, comment=comment, author=token.user, game=game)
    return JsonResponse({'id': review.pk}, status=200)


@correct_method('GET')
@review_exists
def review_detail(request: HttpRequest, review_pk: int) -> HttpResponse:
    review = Review.objects.get(pk=review_pk)
    serializer = ReviewSerializer(review, request=request)
    return serializer.json_response()
