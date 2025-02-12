import re
import json

from django.http import HttpRequest, HttpResponse, JsonResponse

from games.models import Game
from games.serializers import GameSerializer
from orders.models import Order
from shared.decorators import correct_method, order_exists, token_check, user_is_owner, required_fields, game_exists
from users.models import Token

from .serializers import OrderSerializer

# Create your views here.


@correct_method('POST')
@token_check
def add_order(request: HttpRequest) -> HttpResponse:
    payload = request.headers.get('Authorization')
    regexp = r'Bearer\s(?P<token>[\d|a-f]{8}-[\d|a-f]{4}-[\d|a-f]{4}-[\d|a-f]{4}-[\d|a-f]{12})'
    captured_token = re.fullmatch(regexp, payload)['token']
    token = Token.objects.get(key=captured_token)
    review = Order.objects.create(user=token.user)
    return JsonResponse({'id': review.pk}, status=200)


@correct_method('GET')
@token_check
@order_exists
@user_is_owner
def order_detail(request: HttpRequest, order_pk: int) -> HttpResponse:
    order = Order.objects.get(pk=order_pk)
    serializer = OrderSerializer(order, request=request)
    return serializer.json_response()


@correct_method('GET')
@token_check
@order_exists
@user_is_owner
def order_game_list(request: HttpRequest, order_pk: int) -> HttpResponse:
    order = Order.objects.get(pk=order_pk)
    serializer = GameSerializer(order.games.all(), request=request)
    return serializer.json_response()


@correct_method('POST')
@required_fields('game-slug')
@token_check
@order_exists
@game_exists
@user_is_owner
def add_game_to_order(request: HttpRequest, order_pk: int) -> HttpResponse:
    game_slug = json.loads(request.body)['game-slug']
    print(game_slug)
    game = Game.objects.get(slug=game_slug)
    order = Order.objects.get(pk=order_pk)
    order.games.add(game)
    return JsonResponse({'num-games-in-order': order.games.count()}, status=200)
