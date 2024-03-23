from rest_framework import serializers

from api.serializers.category import CategorySerializer, GenreSerializer
from reviews.models import Category, Genre, Title
from reviews.validators import year_is_not_future


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    genre = GenreSerializer(many=True)
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
            'rating',
        )

    # Переопределяю стандартный метод, для вывода информации в заданом формате
    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['category'] = CategorySerializer(instance.category).data
        representation['genre'] = GenreSerializer(
            instance.genre.all(),
            many=True,
        ).data
        return representation


class TitleWriteSerializer(serializers.ModelSerializer):
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
        model = Title
        fields = (
            'id',
            'name',
            'year',
            'description',
            'genre',
            'category',
        )

