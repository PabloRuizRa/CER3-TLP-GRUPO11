from django.shortcuts import render
import requests

# Create your views here.

def home(request):
    title = "Inicio"

    data = {
        "title" : title,
    }

    return render(request, 'core/home.html',data)