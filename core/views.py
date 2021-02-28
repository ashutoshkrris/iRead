from django.shortcuts import render


# Create your views here.
def index(request):
    return render(request, "core/index.html")

def about(request):
    return render(request, "core/about.html")

def contact(request):
    return render(request, "core/contact.html")

def single(request):
    return render(request, "core/single.html")

