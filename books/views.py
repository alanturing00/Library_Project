from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics, status, viewsets, permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import (BooksCatalogsSerializer, BooksSerializer, RentalBookSeriliazer,
                          ReviewSerializer, UserRentalBookSeriliazer, UserProfileUpdateSerializer,
                          UserPasswordChangserializer, ReviewSerializer, UserSerializer,
                           UserProfileserializer, BookSerializer, Bookrentalserializer)
from rest_framework.response import Response
from .models import Book, Review, UserProfile, Rental
from .permissions import IsAdminOrReadOnly, IsAuthorOrReadOnly, IsMyAcountOrReadOnly, IsAdmin
from django.shortcuts import get_object_or_404
from django.views.generic import DetailView
from rest_framework.generics import ListAPIView


# used!
class ChangePasswordView(generics.UpdateAPIView):
    model = User
    serializer_class =UserPasswordChangserializer
    permission_classes = [IsAuthenticated,]
    
    def get_object(self,queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if self.object.check_password(serializer.data.get('old_password')):
                self.object.set_password(serializer.data.get('new_password'))
                self.object.save()
                response ={
                    'status': 'success',
                    'code': status.HTTP_200_OK,
                    'message': 'Your password has been changed succesfully',
                    'data':[]
                }
                return Response(response)
            else:
                Response({'old_password':['wrong password. ']}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


# used!
class BooksCatalogs(generics.ListAPIView):
    serializer_class= BooksCatalogsSerializer
    permission_classes= [IsAuthenticated,]
    
    def get_queryset(self):
        return Book.objects.all()
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user_profile = request.user.userprofile
        user_data = {
            'username': request.user.username,
            'photo': user_profile.user_photo.url if user_profile.user_photo else None
        }
        catalogs = queryset.values_list('cataloge', flat=True).distinct()
        data = {'user': user_data, 'books': list(catalogs)}
        return Response(data)
    

# used!
class BooksByCatalogs(generics.ListAPIView):
    permission_classes= [IsAuthenticated,]
    serializer_class= BooksSerializer 
    
    def get_queryset(self):
        catalogs= self.kwargs['catalogs']
        books= Book.objects.filter(cataloge=catalogs)
        return books
    
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user_profile = request.user.userprofile
        user_data = {
            'username': request.user.username,
            'photo': user_profile.user_photo.url if user_profile.user_photo else None
        }
        data = {'user': user_data, 'books':BooksSerializer(queryset, many= True).data}
        return Response(data)



# used!
class BookDetails(generics.ListCreateAPIView):
    permission_classes= [IsAuthenticated,]
    serializer_class= ReviewSerializer

    def get_queryset(self):
        book= Book.objects.get(isbn= self.kwargs['isbn'])
        review= Review.objects.filter(book= book)
        return review
    
    def list(self, request, *args, **kwargs):
        # profile= UserProfile.objects.get(user= self.request.user)
        user_profile = request.user.userprofile
        user_data = {
            'username': request.user.username,
            'photo': user_profile.user_photo.url if user_profile.user_photo else None
        }
        reviews= self.get_queryset()
        reviews_serializer= ReviewSerializer(reviews, many=True)
        book= Book.objects.get(isbn= self.kwargs['isbn'])
        book_serializer = BooksSerializer(book)
        data = {'user': user_data, 'books': book_serializer.data, 'reviews': reviews_serializer.data}
        return Response(data)
    
    def post(self, request, *args, **kwargs):
        profile= UserProfile.objects.get(user= self.request.user)
        book= Book.objects.get(isbn= self.kwargs['isbn'])
        seriliazer= ReviewSerializer(data= request.data)
        if seriliazer.is_valid():
            seriliazer.save( user= profile, book= book)
            return Response(seriliazer.data, status=status.HTTP_201_CREATED)
        return Response({"error": "an error occurred during save the comment!"}, status=status.HTTP_400_BAD_REQUEST)
    

# used!
class UserProfileView(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = UserProfileserializer

    def get_queryset(self):
        user = self.request.user
        profile = UserProfile.objects.get(user=user)
        return Rental.objects.filter(user=profile)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        user = self.request.user
        profile = UserProfile.objects.get(user=user)
        user_books_serializer = UserRentalBookSeriliazer(queryset, many=True)
        profile_serializer = UserProfileserializer(profile)
        user_serializer = UserSerializer(user)

        data = {
            'user': user_serializer.data['username'],
            'profile': profile_serializer.data,
            'rental_book': user_books_serializer.data
        }
        return Response(data)

# used!
class UserProfileUpdate(generics.RetrieveUpdateAPIView):
    permission_classes= [IsAuthenticated,]
    serializer_class= UserProfileUpdateSerializer

    def get_object(self):
        user= self.request.user
        return UserProfile.objects.get(user=user)


# used!
class RentalBook(generics.CreateAPIView):
    permission_classes= (IsAuthenticated,)
    serializer_class= RentalBookSeriliazer

    def create(self, request, *args, **kwargs):
        profile= UserProfile.objects.get(user= self.request.user)
        book= Book.objects.get(isbn= self.kwargs['isbn'])
        serializer= RentalBookSeriliazer(data= request.data)
        if serializer.is_valid():
            # user only have one object of the same book:
            try:
                B= Rental.objects.get(user= profile, book=book)
                return Response({"error": "You alredy rent this book!"}, status=status.HTTP_400_BAD_REQUEST)
            
            except Rental.DoesNotExist:
                serializer.save(user= profile, book= book)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class UserProfileViews(generics.RetrieveAPIView):
    serializer_class = UserProfileserializer
    def get_queryset(self):
        user_id = self.kwargs['pk']
        return UserProfile.objects.filter(user_id=user_id)

class UserView(generics.RetrieveUpdateAPIView):
    permission_classes =[IsMyAcountOrReadOnly,]
    queryset = User.objects.all()
    serializer_class =UserSerializer

class UserRental(generics.ListAPIView):
    serializer_class= Bookrentalserializer
    def get_queryset(self):
        u = get_object_or_404(UserProfile, user=self.request.user)
        # u= UserProfile.objects.get(self.request.user)
        return Rental.objects.filter(user_id=u)

# book stuff:



class Book_list(generics.ListCreateAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = Book.objects.all()
    permission_classes = [IsAdminOrReadOnly,]
    serializer_class = BookSerializer


class BookReviewList(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated,]
    serializer_class = ReviewSerializer

    def get_queryset(self):
        book_id = self.kwargs['pk']
        return Review.objects.filter(book_id=book_id)
    
    def create(self, request, *args, **kwargs):
        book_id = self.kwargs['pk']
        serializer= ReviewSerializer(data=request.data)
        
        if serializer.is_valid():
            user_profile = get_object_or_404(UserProfile, user=request.user)
            serializer.save(user = user_profile, book_id=book_id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
class BookRentalAdmin(generics.ListCreateAPIView):
    permission_classes= [IsAdmin,]
    serializer_class= Bookrentalserializer
    
    def get_queryset(self):
        book_id= self.kwargs['pk']
        return Rental.objects.filter(book_id=book_id)
    
    def create( self, request, *args, **kwargs):
        book_id= self.kwargs['pk']
        serializer= Bookrentalserializer(data=request.data)

        if serializer.is_valid():
            book= Book.objects.get(id=book_id)
            bookcount= book.copycounts
            if bookcount> 0:
                # serializer.save(user= user_id, book_id= book_id)
                book.copycounts= bookcount-1
                book.save()
                user_profile = get_object_or_404(UserProfile, user=request.user)
                serializer.save(user=user_profile, book_id =book_id)
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            serializer_dict= serializer.data
            serializer_dict['message']= 'sorry! there is no copyes left!'
            return Response(serializer_dict, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookRental(generics.CreateAPIView):
    permission_classes= [IsAuthenticated,]
    serializer_class= Bookrentalserializer
    
    def create(self, request, *args, **kwargs):
        book_id = self.kwargs['pk']
        user_id = get_object_or_404(UserProfile, user=request.user)
        serializer= Bookrentalserializer(data=request.data)
        if serializer.is_valid():
            # if book_id.copycounts >0:
            # if Book[book_id].copycounts >0:
            book= Book.objects.get(id=book_id)
            bookcount= book.copycounts
            if bookcount> 0:
                serializer.save(user= user_id, book_id= book_id)
                book.copycounts= bookcount-1
                book.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            serializer_dict= serializer.data
            serializer_dict['message']='there is no copyes for now! '
            return Response(serializer_dict, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)