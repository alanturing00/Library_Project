from django.urls import path
from .views import ChangePasswordView, Book_list,BookReviewList, UserProfileView,UserView, UserProfileViews, BookRentalAdmin, BookRental, UserRental
from rest_framework.routers import SimpleRouter


urlpatterns = [

    # user stuff:
    path('user/change_password/update/',ChangePasswordView.as_view(),name='changepass'),
    path('user/profile/update/', UserProfileView.as_view(), name='user-profile-update'),
    path('user/<int:pk>/',UserView.as_view(),name= 'user'),
    path('user/profile/books/rental/',UserRental.as_view(),name='userrental'),

    # books stuff:
    path('books/',Book_list.as_view(),name='booklist'),
    path('book/<int:pk>/reviews/', BookReviewList.as_view(), name='book_reviews'),
    path('book/<int:pk>/rental/',BookRental.as_view(),name='bookrental'),
    path('book/<int:pk>/rental/admin_view/',BookRentalAdmin.as_view(),name='bookrentaladmin'),
]
