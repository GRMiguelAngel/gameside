from categories.models import Category
from games.models import Game
import json
from .serializers import JsonResponse

# from django.contrib.auth import get_user_model


def correct_method(func):
    def wrapper(request, *args, **kwargs):
        if request.method != 'GET':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return func(request, *args, **kwargs)

    return wrapper


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


def _(*fields):
    def decorator(func):
        def wrapper(*args, **kwargs):
            request = json.loads(args[0])
            print(request)
            return func(*args, **kwargs)
        return wrapper

# def auth_required(func):
#     def wrapper(request, *args, **kwargs):
#         User = get_user_model()
#         try:
#             payload = json.loads(request.body)
#             user = User.objects.get(token__key=payload.get('token'))
#             request.user = user
#         except User.DoesNotExist:
#             return JsonResponse(
#                 {'error': 'Unknown authentication token'},
#                 status=401,
#             )
#         return func(request, *args, **kwargs)

#     return wrapper