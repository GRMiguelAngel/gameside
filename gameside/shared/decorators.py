from .serializers import JsonResponse
from categories.models import Category


def correct_method(func):
    def wrapper(request, *args, **kwargs):
        if request.method != 'GET':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return func(request, *args, **kwargs)

    return wrapper


def category_exists(func):
    def wrapper(request, *args, **kwargs):
        if Category.objects.get(slug=kwargs['category_slug']):
            return JsonResponse({'error': 'Category not found'}, status=404)
        return func(request, *args, **kwargs)

    return wrapper

