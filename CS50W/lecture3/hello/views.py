from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, "hello/index.html")

def ling(request):
    return HttpResponse("Hello, Chin Ling")

def david(request):
    return HttpResponse("Hello, David")

# def greet2(request, name):
#     return HttpResponse(f"Hello, {name.capitalize()} !")

def greet(request, name):
    return render(request, "hello/greet.html", {"name":name.capitalize()})