from django.http import HttpRequest, HttpResponse

from shared.decorators import correct_method, object_exists

from .models import Platform
from .serializers import PlatformSerializer


# Create your views here.
@correct_method('GET')
def platform_list(request: HttpRequest) -> HttpResponse:
    platforms = Platform.objects.all()
    serializer = PlatformSerializer(platforms, request=request)
    return serializer.json_response()


@correct_method('GET')
@object_exists(Platform)
def platform_detail(request: HttpRequest, platform_slug: str) -> HttpResponse:
    platform = Platform.objects.get(slug=platform_slug)
    serializer = PlatformSerializer(platform, request=request)
    return serializer.json_response()
