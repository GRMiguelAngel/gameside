from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User

from shared.decorators import correct_method
# Create your views here.

@correct_method
def add_order(request: HttpRequest) -> HttpResponse:
    pass