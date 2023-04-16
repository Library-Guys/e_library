from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Pdf_Info, Review
from .form import *
from .recomm import *
# Create your views here.

def digital_books(request, pram = None):
    book = Pdf_Info.objects.all()
    if pram is not None:
        book=book.filter(title__startswith=pram)
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

# @staff_member_required()
def book_detail(request, slug):
    # book = get_object_or_404(Pdf_Info, slug = slug)
    # book = Pdf_Info.objects.get(slug=slug)
    book = Pdf_Info.objects.filter(slug = slug).first()
    # recommendations = get_top_n_recommendations(book, 5)
    # for books in book:
    #     rating = Review.objects.filter(books=books, user=request.user).first()
    #     books.user_rating = rating.rating if rating else 0
    
    if request.method == "POST":
        rating = request.POST.get('rating')
        content = request.POST.get("content",'')
        
        if content:
            reviews = Review.objects.filter(created_by=request.user, book = book)
            
            if reviews.count() > 0:
                review = reviews.first()
                review.rating = rating
                review.content = content
                review.save()
            
            else:
                review = Review.objects.create(
                    book = book,
                    rating = rating,
                    content = content,
                    created_by= request.user
                )
            
            return redirect('books:book_detail', slug = slug)
        
    context = {'book':book}
    
    return render(request, 'books/book_detail.html', context)

# def rate(request, book_id:int, rating:int):
#     book = Pdf_Info.objects.get(id = book_id)
#     Review.objects.filter(book=book, user=request.user, rating=rating)
#     book.rating_set.create(usr= )
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
    
    # #get the user ID
    # user_id = request.user.id
    # #get recommended books
    # recommended_books = recommend_books(user_id)
    
    if book.count() == 0:
        messages.warning(request, 'Search result not found.Please search again.')
    context = {
        'book':book,
        'queries':queries ,
        # 'recommended_books' : recommended_books
    }
    return render(request, 'books/search.html', context)


@login_required
def books_recommended(request):
    #create the user preference and similarity matrices
    user_pref_matrix = create_user_preference_matrix()
    sim_matrix = create_similarity_matrix(user_pref_matrix)
    
    #get the current user's id
    user_id = request.user.id
    
    #make recommendations for the user
    recommended_books = make_recommendations(user_id, user_pref_matrix, sim_matrix)
    
    #render the templates with the recommended books
    context ={
        'recommended_books' : recommended_books
    }
    
    return render(request, 'books:recommendation.html', context)