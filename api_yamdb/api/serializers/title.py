from rest_framework import serializers

from yam_auth.constants import MAX_LENGTH_256
from api.serializers.category import CategorySerializer, GenreSerializer
from reviews.models import Category, Genre, Title
from reviews.validators import year_is_not_future


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

    rating = serializers.IntegerField(read_only=True)

    year = serializers.IntegerField(validators=[year_is_not_future])

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
        for genre_data in genres_data:
            genre, _ = Genre.objects.get_or_create(name=genre_data)
            title.genre.add(genre)

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
