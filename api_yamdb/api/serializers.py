import datetime as d

from django.db.models import Avg
from rest_framework import serializers
from reviews.models import Category, Genre, Title


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = ('name', 'slug')


class GenresSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class TitlesGetSerializer(serializers.ModelSerializer):
    genre = GenresSerializer(many=True, read_only=True)
    category = CategoriesSerializer(read_only=True)
    rating = serializers.SerializerMethodField()

    class Meta:
        model = Title
        fields = ('__all__')

    def get_rating(self, obj):
        reviews = obj.reviews.all()
        if reviews:
            return int(reviews.aggregate(Avg('score'))['score__avg'])

        return None
    # def validate_year(self, value):
    #     year = d.datetime.today().year
    #     if year < value:
    #         raise serializers.ValidationError(
    #             'Creationyear is from future? Call the timepolice!'
    #         )
    #     return value


class TitlesPostSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = ('id', 'name', 'year', 'description', 'genre', 'category',)
        model = Title

    def validate_year(self, value):
        if type(value) is not int:
            raise serializers.ValidationError(
                'Year must be integer value, not string or something.'
            )
        year = d.datetime.today().year
        if year < value:
            raise serializers.ValidationError(
                'Creationyear is from future? Call the timepolice!'
            )
        return value
