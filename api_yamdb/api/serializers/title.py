from datetime import datetime as dt

from django.db.models import Avg
from rest_framework import serializers

from api.serializers.category import CategorySerializer, GenreSerializer
from reviews.models import Category, Genre, GenreTitle, Title


class TitleSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    rating = serializers.SerializerMethodField('get_rating')

    def get_rating(self, obj):
        return obj.reviews.all().aggregate(
            Avg('score')).get(
            'score__avg', 0.0)

    class Meta:
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
            'rating',)

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

    # Переопределяю стандартный метод, для вывода информации в заданом формате
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['genre'] = GenreSerializer(
            instance.genre.all(),
            many=True,
        ).data
        return representation

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
