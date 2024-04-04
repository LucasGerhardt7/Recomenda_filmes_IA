from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'filme/index.html')

def filme(request):
    return render(request, 'filme/filme.html')

def categoria(request):
    return render(request, 'filme/categoria.html')