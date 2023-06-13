from datetime import date

from django.core.validators import RegexValidator, MaxValueValidator
from django.contrib.auth import get_user_model
from django.db import models

from titles.constants import (
    SCORE_CHOICES,
    TEXT_UPPER_BOUND,
)

User = get_user_model()


class CustomBaseModel(models.Model):
    name = models.CharField('Название', max_length=256)
    slug = models.CharField(
        'Слаг',
        max_length=256,
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
    name = models.CharField('Название', max_length=200)
    year = models.IntegerField(
        'Год выпуска',
        # Оставила отрицательные на случай до НЭ
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
    rating = models.IntegerField(
        verbose_name='Рейтинг произведения',
    )

    class Meta:
        verbose_name = 'Тайтл'
        verbose_name_plural = 'Тайтлы'

    def __str__(self):
        return self.name + ', ' + str(self.year)


class Review(models.Model):
    """
    Класс отзыва на произведение.

    Содержит следующие атрибуты:

    title - произведение, к которому написан отзыв
    author - никнейм автора отзыва
    text - текст отзыва
    pub_date - дата публикации отзыва
    score - оценка для произведения
    """
    title = models.ForeignKey(
        Title,
        verbose_name='Произведение(тайтл)',
        on_delete=models.CASCADE,
        related_name='reviewed_title'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    # Не уверена, что это понравится ревьюверам из-за "магического числа" 11
    # Если я правильно понимаю, то choices используется для выпадания списка
    # с читаемыми баллами, как мне кажется это можно упаковать
    # в отдельный кортеж

    score = models.IntegerField(
        verbose_name='Оценка пользователя',
        choices=SCORE_CHOICES,
    )

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'

    def __str__(self):
        return self.text[:TEXT_UPPER_BOUND] + '...'


class Comment(models.Model):
    """
    Класс комментария к отзыву (модели Review).
    
    Содержит следующие атрибуты:

    rewiew - комментируемый отзыв
    author - автор отзыва
    text - текст комментария
    pub_date - дата публикации комментария
    """
    
    review = models.ForeignKey(
        Review,
        verbose_name='Комментируемый отзыв',
        on_delete=models.CASCADE,
        related_name='review'
    )
    author = models.ForeignKey(
        User,
        verbose_name='Автор отзыва',
        on_delete=models.CASCADE,
    )
    text = models.TextField(
        verbose_name='Текст отзыва',
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
    )

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'

    def __str__(self):
        return self.text[:TEXT_UPPER_BOUND] + '...'
