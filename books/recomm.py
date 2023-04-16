#collaborative book recommentaion system using knn
import numpy as np
from sklearn.neighbors import NearestNeighbors
# import sklearn
from .models import Pdf_Info, Review

from scipy.sparse import csr_matrix
# from sklearn.neighbors import NearestNeighbors
############ item base collaborative recomm ################
def create_ratings_matrix():
    """
    Creates a sparse ratings matrix from the review data.
    """
    reviews = Review.objects.all()
    data = []
    rows = []
    cols = []
    for review in reviews:
        data.append(review.rating)
        rows.append(review.book_id)
        cols.append(review.created_by_id)
    ratings_matrix = csr_matrix((data, (rows, cols)))
    return ratings_matrix

def get_top_n_recommendations(book, n):
    """
    Calculates the top-N recommended books for a given book based on item-based collaborative filtering.
    """
    ratings_matrix = create_ratings_matrix()
    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(ratings_matrix)
    book_index = Pdf_Info.objects.filter(pk=book.pk).values_list('id', flat=True)[0]
    distances, indices = knn.kneighbors(ratings_matrix[book_index], n_neighbors=n+1)
    recommended_book_indices = indices[0][1:]
    recommended_books = Pdf_Info.objects.filter(id__in=recommended_book_indices)
    return recommended_books




################## collaborative recommend#################
def create_user_preference_matrix():
    #get all the reviews  
    reviews = Review.objects.all()
    #get all the book
    books = Pdf_Info.objects.all()
    #Create a dictionary to map book titles to column indices
    user_id_to_idx = {user.id: i for i, user in enumerate(User.objects.all())}
    #initialize the user preference matrix with zeros
    user_pref_matrix = np.zeros((len(user_id_to_idx), len(book_title_to_idx)))
    #fill in the user preference matrix with ratings
    for review in reviews:
        user_idx = user_id_to_idx[review.created_by.id]
        book_idx = book_title_to_idz[review.book.title]
        user_pref_matrix[user_idx, book_idx] = review.rating
    
    return user_pref_matrix

def create_similarity_matrix(user_pref_matrix):
    knn = NearestNeighbors(metric='cosine', algorithm='brute')
    knn.fit(user_pref_matrix)
    sim_matrix = knn.kneighbors_graph(user_pref_matrix, mode = 'connectivity')
    return sim_matrix


def make_recommendations(user_id, user_pref_matrix, sim_matrix):
    #Get the row index of the user in the user preference matrix
    user_idx = user_id_to_idx[user_id]
    #Find the indices to the books the user has not rated
    unrated_book_indices = np.where(user_pref_matrix[user_id] == o)[0]
    #Calculate the weighted average rating for each unrated book
    weighted_ratings = np.zeros(len(unrated_book_indices))
    for i, book_idx  in enumerate(unrated_book_indices):
        sim_scores = sim_matrix[user_idx].toarray()[0]
        user_rating = user_pref_matrix[:, book_idx]
        #Only consider users who have rated the book
        nonzero_indices = np.where(user_ratings != 0 )[0]
        if len(nonzero_indices) == 0:
            continue
        
        weights = sim_scores[nonzero_indices]
        ratings = user_rating[nonzero_indices]
        weighted_ratings[i] = np.dot(weights, ratings)/np.sum(weights)
        #sort the unrated books by weighted average rating
        sorted_indices = np.argsort(weighted_ratings)[::-1]
        recommended_boks = [books[unrated_book_indices[i]] for i in sorted_indices]
        
        return recommended_boks
    
    
######################## content based recommendation ##################
# def recommend_books(user_id, num_recommendations=5):
#     # get all reviews made by the user
#     user_reviews = Review.objects.filter(created_by=user_id)

#     # extract the book IDs
#     book_ids = [review.book_id for review in user_reviews]

#     # extract the features for the books
#     book_features = []
#     for book_id in book_ids:
#         book = Pdf_Info.objects.get(id=book_id)
#         book_features.append([book.genre_id, book.is_premium, book.get_rating()])

#     # fit the KNN model
#     knn_model = NearestNeighbors(metric='cosine', algorithm='brute')
#     knn_model.fit(book_features)

#     # get the top recommended books
#     distances, indices = knn_model.kneighbors([book_features[-1]], n_neighbors=num_recommendations+1)
#     recommended_books = []
#     for i in range(1, num_recommendations+1):
#         book_id = book_ids[indices[0][i]]
#         book = Pdf_Info.objects.get(id=book_id)
#         recommended_books.append(book)

#     return recommended_books