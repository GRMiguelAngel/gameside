from .serializers import JsonResponse


def correct_method(func):
    def wrapper(request, *args, **kwargs):
        if request.method != 'GET':
            return JsonResponse({'error': 'Method not allowed'}, status=405)
        return func(request, *args, **kwargs)

    return wrapper
