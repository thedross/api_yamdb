from rest_framework import serializers
from django.core.validators import MaxValueValidator
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
    rating = serializers.IntegerField()

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
            raise serializers.ValidationError("Добавьте хотя бы один жанр.")
        return genre

    def to_representation(self, instance):
        if not hasattr(instance, 'rating'):
            instance.rating = 0
        serializer = TitleSerializer(instance)
        return serializer.data


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
        fields = ('id', 'text', 'author', 'score', 'pub_date')

    def create(self, validated_data):
        if Review.objects.filter(
            title=validated_data.get('title'),
            author=validated_data.get('author')
        ).exists():
            raise serializers.ValidationError(
                'Вы уже написали отзыв к этому произведению.'
            )
        return super().create(validated_data)


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
        fields = ('id', 'text', 'author', 'pub_date')
