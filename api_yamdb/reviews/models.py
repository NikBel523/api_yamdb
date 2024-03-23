from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.constants import (
    MAX_NAME_LENGTH,
    MAX_SCORE,
    MAX_SLUG_LENGTH,
    MIN_SCORE,
)
from reviews.validators import year_is_not_future

User = get_user_model()


class BaseTagModel(models.Model):
    name = models.CharField('Название', max_length=MAX_NAME_LENGTH)
    slug = models.SlugField(
        unique=True,
        max_length=MAX_SLUG_LENGTH,
        db_index=True)

    class Meta:
        abstract = True
        # нужно для повторяемости результата, особенно при пагинации
        ordering = ('slug', )

    def __str__(self):
        return self.name


class Category(BaseTagModel, models.Model):
    pass


class Genre(BaseTagModel, models.Model):
    pass


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=MAX_NAME_LENGTH, db_index=True,
    )
    year = models.SmallIntegerField(
        'Год выпуска', validators=[year_is_not_future])
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='titles', blank=False, null=False
    )

    genre = models.ManyToManyField(Genre)

    class Meta:
        # нужно для повторяемости результата, особенно при пагинации
        ordering = ('name', )

    def __str__(self):
        return self.name


class Review(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)
    text = models.TextField('Текст отзыва')
    score = models.IntegerField(
        'Оценка',
        validators=[
            MinValueValidator(MIN_SCORE),
            MaxValueValidator(MAX_SCORE)])
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['author', 'title'],
                name='one_author_for_title')]
        ordering = ('pub_date', )
        default_related_name = 'reviews'


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE)

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE)

    text = models.TextField('Текст комментария')

    pub_date = models.DateTimeField(
        'Дата комментария', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('pub_date', )
        default_related_name = 'comments'
