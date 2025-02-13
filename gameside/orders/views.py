import json
import re

from django.http import HttpRequest, HttpResponse, JsonResponse

from games.models import Game
from games.serializers import GameSerializer
from orders.models import Order
from shared.decorators import (
    correct_method,
    game_exists,
    order_exists,
    required_fields,
    token_check,
    user_is_owner,
    invalid_status,
    is_initiated,
    valid_card,
    is_confirmed
)
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
    game = Game.objects.get(slug=game_slug)
    order = Order.objects.get(pk=order_pk)
    order.games.add(game)
    return JsonResponse({'num-games-in-order': order.games.count()}, status=200)


@correct_method('POST')
@required_fields('status')
@token_check
@order_exists
@user_is_owner
@invalid_status
@is_initiated
def change_order_status(request: HttpRequest, order_pk: int) -> HttpResponse:
    status = json.loads(request.body)['status']
    order = Order.objects.get(pk=order_pk)
    order.status = status
    order.save()
    return JsonResponse({'status': order.get_status_display()}, status=200)

@correct_method('POST')
@required_fields('card-number','exp-date', 'cvc')
@token_check
@order_exists
@user_is_owner
@valid_card
@is_confirmed
def pay_order(request: HttpRequest, order_pk: int) -> HttpResponse:
    order = Order.objects.get(pk=order_pk)
    order.status = Order.Status.PAID
    order.save()
    return JsonResponse({'status': order.get_status_display()}, status=200)