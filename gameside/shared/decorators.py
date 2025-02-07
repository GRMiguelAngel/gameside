from categories.models import Category
from games.models import Game
import json
from .serializers import JsonResponse

# from django.contrib.auth import get_user_model

def correct_method(method):
    def decorator(func):
        def wrapper(request, *args, **kwargs):
            if request.method != method:
                return JsonResponse({'error': 'Method not allowed'}, status=405)
            return func(request, *args, **kwargs)

        return wrapper
    return decorator

def category_exists(func):
    def wrapper(request, *args, **kwargs):
        try:
            Category.objects.get(slug=kwargs['category_slug'])
        except:
            return JsonResponse({'error': 'Category not found'}, status=404)
        return func(request, *args, **kwargs)

    return wrapper


def game_exists(func):
    def wrapper(request, *args, **kwargs):
        try:
            Game.objects.get(slug=kwargs['game_slug'])
        except:
            return JsonResponse({'error': 'Game not found'}, status=404)
        return func(request, *args, **kwargs)

    return wrapper


def required_fields(*fields):
    def decorator(func):
        def wrapper(*args, **kwargs):
            request_body = json.loads(args[0].body)
            for field in fields:
                if field not in request_body:
                    return JsonResponse({'error': 'Missing required fields'}, status=400)
            return func(*args, **kwargs)
        return wrapper
    return decorator