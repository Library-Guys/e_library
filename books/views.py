from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from .models import Pdf_Info, Review
from .form import *
from .recomm import *
import pickle
import numpy as np
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


def book_detail(request, slug):
    # book = get_object_or_404(Pdf_Info, slug = slug)
    # book = Pdf_Info.objects.get(slug=slug)
    book = Pdf_Info.objects.filter(slug = slug).first()
    # books.user_rating = rating.rating if rating else 0
    
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
        'queries':queries ,
        # 'recommended_books' : recommended_books
    }
    return render(request, 'books/search.html', context)



# @app.route()
def recommend(request):
    # books = Pdf_Info.objects.all()
    popular_df = pickle.load(open('popular.pkl', 'rb'))
    pt = pickle.load(open('pt.pkl', 'rb'))
    books = pickle.load(open('books.pkl', 'rb'))
    similarity_scores= pickle.load(open('similarity_scores.pkl', 'rb'))
    # index = None
    if request.method == 'POST':
        # index fetch
        user_input = request.POST.get('user_input')
        # index = np.where(pt.index == user_input)[0][0]
        index_array = np.where(pt.index == user_input)[0]
        if len(index_array) > 0:
            index = index_array[0]
            # Rest of the code
        
            similar_items = sorted(list(enumerate(similarity_scores[index])),key=lambda x:x[1],reverse=True)[1:9]
        
            data = []
            for i in similar_items:
                item = []
                temp_df = books[books['title'] == pt.index[i[0]]]
                item.extend(list(temp_df.drop_duplicates('title')['title'].values))
                item.extend(list(temp_df.drop_duplicates('title')['author'].values))
                item.extend(list(temp_df.drop_duplicates('title')['image'].values))
                # item.extend(list(temp_df.drop_duplicates('title')['image'].apply(lambda x: f"/media/{x}").values))

                
                data.append(item)
            
            print(data)
            
            context = {
                'data' : data
            }
            return render(request, 'books/recommendation.html', context)
        else:
            messages.info(request, 'recommendation not found')
            
    return render(request, 'books/recommendation.html')


# def book_recommendations(request):
#     # Get the top 10 recommended books for the given user ID
#     recommendations = recommend_books(picked_user_id)

#     # Convert the recommendations dataframe to a list of book titles
#     books = recommendations['book'].tolist()

#     # Render the book recommendations template with the list of recommended books
#     return render(request, 'books/book_recommendations.html', {'books': books})
def book_recommendations(request):
    # Get the current user ID
    user_id = request.user.id

    # Load the necessary data
    popular_df = pickle.load(open('popular.pkl', 'rb'))
    pt = pickle.load(open('pt.pkl', 'rb'))
    books = pickle.load(open('books.pkl', 'rb'))
    similarity_scores= pickle.load(open('similarity_scores.pkl', 'rb'))
    matrix = pickle.load(open('matrix.pkl', 'rb'))

    # Check if the user ID exists in the matrix dataframe
    if user_id in matrix.index:
        # Get the top 10 recommended books for the given user ID
        recommendations = recommend_books(request)

        # Convert the recommendations dataframe to a list of book titles
        books = recommendations['book'].tolist()

        # Render the book recommendations template with the list of recommended books
        return render(request, 'books/book_recommendations.html', {'books': books})
    else:
        # If the user ID does not exist in the matrix dataframe, return an error message
        # return render(request, 'error.html', {'message': 'User ID not found in ratings data'})
        messages.info(request, 'No recommendation found')