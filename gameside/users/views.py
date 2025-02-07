import json

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

# payload = request.headers.get('Authorization')
# valid_token = r'^Bearer [0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$'
# regexp = re.fullmatch(valid_token, payload)
# if not :
# return JsonResponse({'error': 'Invalid authentication token'}, status=400)


@require_POST
@csrf_exempt
def auth(request):
    data = json.loads(request.body)
    username, password = data['username'], data['password']
    if user := authenticate(username=username, password=password):
        return JsonResponse({'token': user.token.key})

    return JsonResponse({'error': 'Invalid credentials'}, status=401)
