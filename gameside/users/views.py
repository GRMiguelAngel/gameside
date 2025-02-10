import json

from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from shared.decorators import correct_method, required_fields

# payload = request.headers.get('Authorization')
# valid_token = r'^Bearer [0-9a-f]{8}-[0-9a-f]{4}-[0-5][0-9a-f]{3}-[089ab][0-9a-f]{3}-[0-9a-f]{12}$'
# regexp = re.fullmatch(valid_token, payload)
# if not :


@correct_method('POST')
@required_fields('username', 'password')
@csrf_exempt
def auth(request):
    data = json.loads(request.body)
    username, password = data['username'], data['password']
    if user := authenticate(username=username, password=password):
        return JsonResponse({'token': user.token.key})

    return JsonResponse({'error': 'Invalid credentials'}, status=401)
