import json

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import correct_method, required_fields


@correct_method('POST')
@required_fields('username', 'password')
@csrf_exempt
def auth(request):
    data = json.loads(request.body)
    username, password = data['username'], data['password']
    if user := authenticate(username=username, password=password):
        return JsonResponse({'token': user.token.key})

    return JsonResponse({'error': 'Invalid credentials'}, status=401)
