from django.core.validators import MaxValueValidator
from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import (
    Category,
    Comment,
    Genre,
    Review,
    Title,
)
from reviews.utils import get_current_year


class GenreSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Genre.
    """
    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategorySerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Category.
    """
    class Meta:
        model = Category
        fields = ('name', 'slug')


class TitleSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Title.
    """
    genre = GenreSerializer(many=True)
    category = CategorySerializer()
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        model = Title
        fields = '__all__'


class TitleCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для содания модели Title.
    """
    genre = SlugRelatedField(
        label='Жанры',
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = SlugRelatedField(
        label='Категория',
        queryset=Category.objects.all(),
        slug_field='slug',
    )
    year = serializers.IntegerField(
        label='Год выпуска',
        validators=[
            MaxValueValidator(
                limit_value=get_current_year,
                message='Год выпуска не может быть больше текущего года.'
            )
        ]
    )

    class Meta:
        model = Title
        fields = '__all__'

    def validate_genre(self, genre):
        if not genre:
            raise serializers.ValidationError('Добавьте хотя бы один жанр.')
        return genre

    def to_representation(self, instance):
        return TitleSerializer(instance).data


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Review.
    """
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title', )

    def validate(self, data):
        request = self.context.get('request')
        if (
            request.method == 'POST'
            and Review.objects.filter(
                title=request.parser_context.get('kwargs').get('title_id'),
                author=request.user
            ).exists()
        ):
            raise serializers.ValidationError(
                'Вы уже написали отзыв к этому произведению.'
            )
        return super().validate(data)


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Comment.
    """
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review', )
