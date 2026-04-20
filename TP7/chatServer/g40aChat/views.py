from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

# Create your views here.

def deconnect(request):
        return render(request,template_name="deconnect.html")

@login_required
def accueil(request):
    return render(request,template_name="accueil.html")
