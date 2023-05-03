from django.http import HttpResponse
from django.shortcuts import render


# Create your views here.
def hello(request):
    if request.method == 'GET':
        return HttpResponse("hello")
