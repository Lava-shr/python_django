from rest_framework import serializers
from .models import *


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ('full_name', 'email', 'university_studies', 'dob', 'status')


class UserimageSerializer(serializers.ModelSerializer):
    user = UsersSerializer()

    class Meta:
        model = Userimage
        fields = '__all__'
       

class UniversitiesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Universities
        fields = '__all__'


class UniimageSerializer(serializers.ModelSerializer):
    uni = UniversitiesSerializer()

    class Meta:
        model = Uniimage
        fields = '__all__'


class UnitofstudySerializer(serializers.ModelSerializer):
    uni = UniversitiesSerializer()

    class Meta:
        model = Unitofstudy
        fields = '__all__'


class ReviewsSerializer(serializers.ModelSerializer):
    uni = UniversitiesSerializer()
    user = UsersSerializer()

    class Meta:
        model = Reviews
        fields = '__all__'


class ExperienceSerializer(serializers.ModelSerializer):
    user = UsersSerializer()
    uos = UnitofstudySerializer()

    class Meta:
        model = Experience
        fields = '__all__'


class CommentsSerializer(serializers.ModelSerializer):
    users = UsersSerializer()
    reviews = ReviewsSerializer()

    class Meta:
        model = Comments
        fields = '__all__'

