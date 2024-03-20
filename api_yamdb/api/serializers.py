from datetime import datetime as dt
from rest_framework.validators import UniqueTogetherValidator
from django.shortcuts import get_object_or_404
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
        # fields = '__all__'
        fields = ('id', 'text', 'author', 'score', 'title', 'pub_date')
        read_only_fields = ('title', )

    def validate(self, attrs):
        method = self.context['request'].method
        current_user = self.context['request'].user
        title_id = self.context['view'].kwargs.get('title_id')
        if method == 'POST':
            if title_id is not None:
                existing_reviews = Review.objects.filter(
                    author=current_user,
                    title=title_id,
                )
                if existing_reviews.exists():
                    raise serializers.ValidationError('Отзыв уже есть.')
        # if method == 'PATCH':
        #     review_id = self.context['view'].kwargs.get('review_id')
        #     review = get_object_or_404(Review, id=review_id)
        #     if current_user != review.author:
        #         raise serializers.ValidationError('Нельзя менять чужой отзыв.')
            

        return attrs


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
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        model = Title
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
