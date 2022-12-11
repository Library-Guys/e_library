from django.shortcuts import render, redirect
from .models import *


# Create your views here.

def items(request):
    book = Pdf_Info.objects.all()
    context = {
        'book':book
    }

    return render(request, 'books/home.html', context)