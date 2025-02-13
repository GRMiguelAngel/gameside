import json
import re

from django.http import JsonResponse

from categories.models import Category
from games.models import Game, Review
from orders.models import Order
from platforms.models import Platform
from users.models import Token

# from django.contrib.auth import get_user_model


def correct_method(method):
    def decorator(func):
        def wrapper(*args, **kwargs):
            if args[0].method != method:
                return JsonResponse({'error': 'Method not allowed'}, status=405)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def category_exists(func):
    def wrapper(*args, **kwargs):
        try:
            Category.objects.get(slug=kwargs['category_slug'])
        except Category.DoesNotExist:
            return JsonResponse({'error': 'Category not found'}, status=404)
        return func(*args, **kwargs)

    return wrapper


def game_exists(func):
    def wrapper(*args, **kwargs):
        try:
            game_slug = json.loads(args[0].body)['game-slug']
        except:
            game_slug = kwargs['game_slug']
        try:
            Game.objects.get(slug=game_slug)
        except Game.DoesNotExist:
            return JsonResponse({'error': 'Game not found'}, status=404)
        return func(*args, **kwargs)

    return wrapper


def platform_exists(func):
    def wrapper(*args, **kwargs):
        try:
            Platform.objects.get(slug=kwargs['platform_slug'])
        except Platform.DoesNotExist:
            return JsonResponse({'error': 'Platform not found'}, status=404)
        return func(*args, **kwargs)

    return wrapper


def review_exists(func):
    def wrapper(*args, **kwargs):
        try:
            Review.objects.get(pk=kwargs['review_pk'])
        except Review.DoesNotExist:
            return JsonResponse({'error': 'Review not found'}, status=404)
        return func(*args, **kwargs)

    return wrapper


def order_exists(func):
    def wrapper(*args, **kwargs):
        try:
            Order.objects.get(pk=kwargs['order_pk'])
        except Order.DoesNotExist:
            return JsonResponse({'error': 'Order not found'}, status=404)
        return func(*args, **kwargs)

    return wrapper


def required_fields(*fields):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                request_body = json.loads(args[0].body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid JSON body'}, status=400)
            for field in fields:
                if field not in request_body:
                    return JsonResponse({'error': 'Missing required fields'}, status=400)
            return func(*args, **kwargs)

        return wrapper

    return decorator


def token_check(func):
    def wrapper(*args, **kwargs):
        regexp = r'Bearer\s(?P<token>[\d|a-f]{8}-[\d|a-f]{4}-[\d|a-f]{4}-[\d|a-f]{4}-[\d|a-f]{12})'
        payload = args[0].headers.get('Authorization')
        if not (captured_token := re.fullmatch(regexp, payload)):
            return JsonResponse({'error': 'Invalid authentication token'}, status=400)
        try:
            Token.objects.get(key=captured_token['token'])
        except Token.DoesNotExist:
            return JsonResponse({'error': 'Unregistered authentication token'}, status=401)

        return func(*args, **kwargs)

    return wrapper


def invalid_status(func):
    def wrapper(*args, **kwargs):
        status = json.loads(args[0].body)['status']
        if status not in [Order.Status.CONFIRMED, Order.Status.CANCELLED]:
            return JsonResponse({'error': 'Invalid status'}, status=400)

        return func(*args, **kwargs)

    return wrapper


def is_initiated(func):
    def wrapper(*args, **kwargs):
        order_pk = kwargs['order_pk']
        order = Order.objects.get(pk=order_pk)

        if order.status != Order.Status.INITIATED:
            return JsonResponse(
                {'error': 'Orders can only be confirmed/cancelled when initiated'}, status=400
            )

        return func(*args, **kwargs)

    return wrapper


def is_confirmed(func):
    def wrapper(*args, **kwargs):
        order_pk = kwargs['order_pk']
        order = Order.objects.get(pk=order_pk)

        if order.status != Order.Status.CONFIRMED:
            return JsonResponse(
                {'error': 'Orders can only be paid when confirmed'}, status=400
            )

        return func(*args, **kwargs)

    return wrapper



def user_is_owner(func):
    def wrapper(*args, **kwargs):
        regexp = r'Bearer\s(?P<token>[\d|a-f]{8}-[\d|a-f]{4}-[\d|a-f]{4}-[\d|a-f]{4}-[\d|a-f]{12})'
        payload = args[0].headers.get('Authorization')
        captured_token = re.fullmatch(regexp, payload)['token']
        token = Token.objects.get(key=captured_token)
        order = Order.objects.get(pk=kwargs['order_pk'])
        if not order.user == token.user:
            return JsonResponse({'error': 'User is not the owner of requested order'}, status=403)
        return func(*args, **kwargs)

    return wrapper


def valid_card(func):
    def wrapper(*args, **kwargs):
        data = json.loads(args[0].body)
        card_number, exp_date, cvc = data['card-number'], data['exp-date'], data['cvc']
        card_regexp = r'\d{4}-\d{4}-\d{4}-\d{4}'
        captured_card_number = re.fullmatch(card_regexp, card_number)
        if not captured_card_number:
            return JsonResponse({'error': 'Invalid card number'}, status=400)
        
        exp_date_regexp = r'\d{2}/\d{4}'
        captured_exp_date = re.fullmatch(exp_date_regexp, exp_date)
        if not captured_exp_date:
            return JsonResponse({'error': 'Invalid expiration date'}, status=400)

        cvc_regexp = r'\d{3}'
        captured_cvc = re.fullmatch(cvc_regexp, cvc)
        if not captured_cvc:
            return JsonResponse({'error': 'Invalid CVC'}, status=400)



        return func(*args, **kwargs)

    return wrapper
