import re
from django.shortcuts import render
from users.models import Token
from orders.models import Order
from django.http import HttpRequest, HttpResponse, JsonResponse

from shared.decorators import correct_method, token_check
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

