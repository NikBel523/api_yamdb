from datetime import datetime as dt

from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.constants import (
    MAX_NAME_LENGTH,
    MAX_SCORE,
    MAX_SLUG_LENGTH,
    MIN_SCORE,
)

_User = get_user_model()


class BaseTagModel(models.Model):
    slug = models.SlugField(unique=True, max_length=MAX_SLUG_LENGTH)

    class Meta:
        abstract = True
        # нужно для повторяемости результата, особенно при пагинации
        ordering = ('slug', )

    def __str__(self):
        return self.name


class Category(BaseTagModel, models.Model):
    name = models.CharField('Имя категории', max_length=MAX_NAME_LENGTH)


class Genre(BaseTagModel, models.Model):
    name = models.CharField('Имя жанра', max_length=MAX_NAME_LENGTH)


class Title(models.Model):
    name = models.CharField(
        'Название произведения',
        max_length=MAX_NAME_LENGTH,
    )
    year = models.SmallIntegerField(
        'Год выпуска', validators=[
            MaxValueValidator(limit_value=dt.now().year)])
    description = models.TextField('Описание', null=True, blank=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='titles', blank=False, null=False
    )
    # TODO замечание из ревью не исправил
    genre = models.ManyToManyField(
        Genre, through='GenreTitle')

    class Meta:
        # нужно для повторяемости результата, особенно при пагинации
        ordering = ('category__slug', )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    author = models.ForeignKey(
        _User, on_delete=models.CASCADE)
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
        _User, on_delete=models.CASCADE)

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE)

    text = models.TextField('Текст комментария')

    pub_date = models.DateTimeField(
        'Дата комментария', auto_now_add=True, db_index=True
    )

    class Meta:
        ordering = ('pub_date', )
        default_related_name = 'comments'
