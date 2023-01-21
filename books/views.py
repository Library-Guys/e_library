from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
# from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import *
from .form import *


# Create your views here.

def digital_books(request):
    book = Pdf_Info.objects.all()
    context = {
        'book':book
    }

    return render(request, 'books/home.html', context)

def view_book(request):
    book = Pdf_Info.objects.all()
    context={
        'book':book
    }
    return render(request, 'books/view_books.html', context)



# @login_required()
@staff_member_required()
def add_Book(request,pk=None):
    form = BookForm()#improt productform form form.py
    if request.method == 'POST':
        form = BookForm(request.POST,request.FILES)#request.File send request to the file to be uploaded to uploade the file, without it there would be error while saving file
        print(form)
        if form.is_valid():
            review = form.save(commit=False)
            review.save()
            messages.success(request, 'product added succcssfully')
            return redirect('books:digital_books')
        else:
            messages.error(request, 'Failed to add Product')
    
    context = {
        'form':form
    }
    return render(request, 'books/addbook.html', context)

@staff_member_required()
def book_detail(request, slug):
    book = get_object_or_404(Pdf_Info, slug = slug)
    
    context = {'book':book}
    return render(request, 'books/book_detail.html', context)

@staff_member_required()
def delete_book(request, pk):
    book = Pdf_Info.objects.filter(id = pk)
    
    # if request. != item.created_by:
    #     messages.INFO(request, 'You are not authorized')
    
    if request.method == 'POST':
        book.delete()
        return redirect('books:digital_books')

    context = {
        'book':book
    }
    return render(request, 'books/delete.html', context)



def search(request):
    queries = request.GET.get('query', False)# here 'query' is from 'name= query' in navbar
    if len(queries) > 50:
        book = Pdf_Info.objects.none()
    else:
        book = Pdf_Info.objects.filter(title__icontains = queries)
    
    if book.count() == 0:
        messages.warning(request, 'Search result not found.Please search again.')
    context = {
        'book':book,
        'queries':queries 
    }
    return render(request, 'books/search.html', context)