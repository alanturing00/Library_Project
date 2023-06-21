from django.urls import path
from .views import (BooksCatalogs, BooksByCatalogs, BookDetails, RentalBook, UserProfileUpdate
                    ,ChangePasswordView, Book_list,BookReviewList, UserProfileView,UserView, UserProfileViews, BookRentalAdmin, BookRental, UserRental)
from rest_framework.routers import SimpleRouter


urlpatterns = [

    # user stuff:

    # for changing  the user password:
    path('user/change_password/update/',ChangePasswordView.as_view(),name='changepass'),


    
    # path('user/<int:pk>/',UserView.as_view(),name= 'user'),
    # path('user/profile/books/rental/',UserRental.as_view(),name='userrental'),

    # books stuff:

    # to veiw all the catalogs of the books:
    path("books/catalogs/", BooksCatalogs.as_view(), name="catalogname"),

    # to view the book of the catalog:
    path("books/catalogs/<str:catalogs>/", BooksByCatalogs.as_view(), name="books"),

    # to view the book details:
    path("books/catalogs/<str:catalogs>/<str:isbn>/", BookDetails.as_view(), name="bookdetails"),

    # to view the rental page:
    path("books/catalogs/<str:catalogs>/<str:isbn>/rental/", RentalBook.as_view(), name="rentalbook"),

    # to veiw the user profile:
    path('user/profile/', UserProfileView.as_view(), name='userprofile'),

    # to edite the user profiel information:
    path("user/profile/update/", UserProfileUpdate.as_view(), name="userprofileupdate"),


    path('books/',Book_list.as_view(),name='booklist'),
    path('book/<int:pk>/reviews/', BookReviewList.as_view(), name='book_reviews'),
    path('book/<int:pk>/rental/',BookRental.as_view(),name='bookrental'),
    path('book/<int:pk>/rental/admin_view/',BookRentalAdmin.as_view(),name='bookrentaladmin'),
]
