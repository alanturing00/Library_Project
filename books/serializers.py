from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Book, Review,UserProfile, Rental

# user stuff:
class UserPasswordChangserializer(serializers.Serializer):
    model = User
    old_password = serializers.CharField(required =True)
    new_password = serializers.CharField(required =True) 

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username','first_name', 'last_name', 'email']

class UserProfileserializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)
    # fields = ['address', 'user_photo', 'user']
    class Meta:
        model = UserProfile
        fields = ['address', 'user_photo','user']
    def update(self, instance, validated_data):
        instance.address = validated_data.get('address', instance.address)
        instance.user_photo = validated_data.get('user_photo', instance.user_photo)
        instance.save()
        return instance

class UserProfileForReview(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['user_photo','id']


# Book Stuff


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields= '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    user_review_of_five = serializers.IntegerField(required=True)
    user_review_comment = serializers.CharField(required=True)
    book = BookSerializer(read_only=True)
    user = UserProfileForReview(read_only=True)
    class Meta:
        model = Review
        fields = '__all__'

class Bookrentalserializer(serializers.ModelSerializer):
    date_to= serializers.DateField(required= True)
    additional_information= serializers.CharField(required=True)
    user= UserProfileForReview(read_only= True)
    book= BookSerializer(read_only= True)
    class Meta:
        model =Rental
        fields =['id', 'date_rental', 'date_to', 'additional_information', 'book', 'user']












