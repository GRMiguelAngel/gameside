from django.http import HttpRequest, HttpResponse

from shared.decorators import correct_method, category_exists


from .models import Category
from .serializers import CategorySerializer

# Create your views here.


@correct_method
def category_list(request: HttpRequest) -> HttpResponse:
    category = Category.objects.all()
    serializer = CategorySerializer(category, request=request)
    return serializer.json_response()

@correct_method
@category_exists
def category_detail(request: HttpRequest, category_slug: int) -> HttpResponse:
    category = Category.objects.get(slug=category_slug)
    serializer = CategorySerializer(category, request=request)
    return serializer.json_response()
