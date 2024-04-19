from django.shortcuts import render
from django.http import HttpResponse

def landing_page(request):
    # return HttpResponse('Hello World')
    return render(request, 'landing.html')