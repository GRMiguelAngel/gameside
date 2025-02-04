import re

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

@require_POST
@csrf_exempt
def auth(request):
    payload = request.headers.get('Authorization')
    print(payload)
    TOKEN = r'^[0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$'
    valid_token = re.fullmatch(
        
    )
    if authenticate(username=payload['username'], password=payload['password']):
        return JsonResponse({'token': valid_token})
    return JsonResponse({'error': 'Invalid credentials'}, status=401)
