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
            Game.objects.get(slug=kwargs['game_slug'])
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
