from django.http import HttpRequest, HttpResponse

from shared.decorators import correct_method, object_exists


from .models import Category
from .serializers import CategorySerializer

# Create your views here.


@correct_method('GET')
def category_list(request: HttpRequest) -> HttpResponse:
    category = Category.objects.all()
    serializer = CategorySerializer(category, request=request)
    return serializer.json_response()

@correct_method('GET')
@object_exists('Category')
def category_detail(request: HttpRequest, category_slug: int) -> HttpResponse:
    category = Category.objects.get(slug=category_slug)
    serializer = CategorySerializer(category, request=request)
    return serializer.json_response()
