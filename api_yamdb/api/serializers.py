from datetime import datetime as dt

from rest_framework import serializers
from titles.models import Category, Comment, Genre, GenreTitle, Review, Title


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('name', 'slug',)
        lookup_field = 'slug'
        extra_kwargs = {
            'url': {'lookup_field': 'slug'}
        }


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title', )


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review', )


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='name'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='name',
        many=True
    )

    class Meta:
        model = Title
        # Не использую fields = '__all__'
        # Переопределения полей изменит их порядок в ответах
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')

    def create(self, validated_data):
        # Из уже проверенных данных, получаю список жанров и категорию.
        genres_data = validated_data.pop('genre')
        category_data = validated_data.pop('category')

        # С помощью категории создаю произведение
        category = Category.objects.get(name=category_data)
        title = Title.objects.create(category=category, **validated_data)

        # К новому произведению добавляется информация о связанных жанрах
        for genre_name in genres_data:
            genre = Genre.objects.get(name=genre_name)
            GenreTitle.objects.create(genre=genre, title=title)

        return title

    def validate_year(self, value):
        if value > dt.now().year:
            raise serializers.ValidationError(
                'Год выпуска произведения не может быть больше текущего года.'
            )
        return value

    def validate_name(self, value):
        if len(value) > 256:
            raise serializers.ValidationError(
                'Слишком длинное название.'
            )
        return value
