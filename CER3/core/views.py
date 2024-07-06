from django.shortcuts import render
from django.http import HttpRequest

# Create your views here.

def home(request: HttpRequest):
    title = "Inicio"

    data = {
        "title" : title,
    }

    return render(request, 'core/base.html',data)