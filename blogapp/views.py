from django.shortcuts import render

# Create your views here.

def index(request):
    return render(request, 'index.html')

def blogMain(request):
    return render(request, 'blogMain.html')