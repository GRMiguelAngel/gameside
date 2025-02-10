import json
import re

from django.http import HttpRequest, HttpResponse, JsonResponse

from shared.decorators import correct_method, game_exists, required_fields, review_exists

from .models import Game, Review
from users.models import Token
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
    json_body = json.loads(request.body)
    payload = request.headers.get('Authorization')
    rating, comment = json_body['rating'], json_body['comment']
    regexp = r'Bearer\s(?P<token>[\d|a-f]{8}-[\d|a-f]{4}-[\d|a-f]{4}-[\d|a-f]{4}-[\d|a-f]{12})'
    if not (captured_token := re.fullmatch(regexp, payload)):
        return JsonResponse({'error': 'Invalid authentication token'}, status=400)
    try:
        token = Token.objects.get(key=captured_token['token'])
    except:
        return JsonResponse({'error': 'Unregistered authentication token'}, status=401)
    game = Game.objects.get(slug=game_slug)
    review = Review.objects.create(rating=rating, comment=comment, author=token.user, game=game)
    serializer = ReviewSerializer(review)
    return serializer.json_response()



@correct_method('GET')
@review_exists
def review_detail(request: HttpRequest, review_pk: int) -> HttpResponse:
    review = Review.objects.get(pk=review_pk)
    serializer = ReviewSerializer(review, request=request)
    return serializer.json_response()
