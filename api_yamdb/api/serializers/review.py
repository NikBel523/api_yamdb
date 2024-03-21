from rest_framework import serializers
from reviews.models import Comment, Review


class ReviewSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        model = Review
        fields = ('id', 'text', 'author', 'score', 'pub_date')

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
        return attrs


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        slug_field='username', read_only=True,
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review', )
