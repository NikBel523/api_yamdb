from custom_auth.models import CustomUser
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField('Имя категории', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Genre(models.Model):
    name = models.CharField('Имя жанра', max_length=256)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
        return self.name


class Title(models.Model):
    name = models.CharField('Название произведения', max_length=256)
    year = models.IntegerField('Год выпуска')
    description = models.TextField('Описание')
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE,
        related_name='titles', blank=False, null=False
    )
    genre = models.ManyToManyField(
        Genre, through='GenreTitle')

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    title = models.ForeignKey(Title, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.genre} {self.title}'


class Review(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='reviews'
    )
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews'
    )
    text = models.TextField('Текст отзыва')
    score = models.IntegerField('Оценка', validators=[MinValueValidator(1),
                                                      MaxValueValidator(10)])
    pub_date = models.DateTimeField(
        'Дата публикации', auto_now_add=True, db_index=True
    )


class Comment(models.Model):
    author = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE, related_name='comments'
    )

    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='comments'
    )

    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments'
    )

    text = models.TextField('Текст комментария')

    pub_date = models.DateTimeField(
        'Дата комментария', auto_now_add=True, db_index=True
    )
