from datetime import date

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, RegexValidator
from django.db import models

User = get_user_model()


class CustomBaseModel(models.Model):
    name = models.CharField(
        'Название',
        max_length=settings.DEFAULT_NAME_LENGTH
    )
    slug = models.CharField(
        'Слаг',
        max_length=settings.DEFAULT_SLUG_LENGTH,
        unique=True,
        validators=[
            RegexValidator(
                regex='^[-a-zA-Z0-9_]+$',
                message='Слаг содержит недопустимые символы.'
            )
        ]
    )

    def __str__(self):
        return self.name

    class Meta:
        abstract = True
        ordering = ('name', )


class Genre(CustomBaseModel):
    class Meta(CustomBaseModel.Meta):
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Category(CustomBaseModel):
    class Meta(CustomBaseModel.Meta):
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Title(models.Model):
    name = models.CharField(
        'Название',
        max_length=settings.DEFAULT_NAME_LENGTH
    )
    year = models.IntegerField(
        'Год выпуска',
        validators=[
            MaxValueValidator(
                limit_value=date.today().year,
                message='Год выпуска не может быть больше текущего года.'
            )
        ]
    )
    description = models.TextField('Описание', blank=True)
    category = models.ForeignKey(
        'Category',
        verbose_name='Категория',
        on_delete=models.SET_NULL,
        related_name='category',
        null=True
    )
    genre = models.ManyToManyField(
        'Genre',
        verbose_name='Жанр',
        related_name='genres',
    )

    class Meta:
        verbose_name = 'Тайтл'
        verbose_name_plural = 'Тайтлы'

    def __str__(self):
        return self.name + ', ' + str(self.year)


class Review(models.Model):
    title = models.ForeignKey(
        'Title',
        verbose_name='Тайтл',
        on_delete=models.CASCADE,
        related_name='reviewed_title'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,

    )
    text = models.TextField('Текст')

    SCORE_CHOICES = [
        (score, str(score)) for score in range(1, settings.DEFAULT_SCORE)
    ]

    score = models.IntegerField('Рейтинг', choices=SCORE_CHOICES)

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:settings.DEFAULT_STR_LENGTH] + '...'


class Comment(models.Model):
    title = models.ForeignKey(
        'Title',
        verbose_name='Тайтл',
        on_delete=models.CASCADE,
        related_name='commented_title'
    )
    review = models.ForeignKey(
        'Review',
        verbose_name='Отзыв',
        on_delete=models.CASCADE,
        related_name='review'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор',
        on_delete=models.CASCADE,

    )
    text = models.TextField('Текст')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:settings.DEFAULT_STR_LENGTH] + '...'
