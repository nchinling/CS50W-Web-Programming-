from django.shortcuts import render
from django.http import HttpResponse


 # Create your views here.

# def index(request):
#      return HttpResponse("<h1 style=\"color:blue\">Hello, world!</h1>")

def index(request):
    return render(request, "myapp/index.html")

def brian(request):
    return HttpResponse("Hello, Brian!")

def david(request):
    return HttpResponse("Hello, David!")

def greet(request, name):
    return render(request, "myapp/greet.html", {
        "name": name.capitalize()
    })