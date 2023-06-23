from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from titles.models import (
    Title,
    Genre,
    Category,
    Review,
    Comment,
)


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

    class Meta:
        model = Title
        exclude = ('rating', )


class TitleCreateSerializer(serializers.ModelSerializer):
    """
    Сериализатор для содания модели Title.
    """
    genre = SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )
    category = SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
    )

    class Meta:
        model = Title
        exclude = ('rating', )


class ReviewSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Review.
    """
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    title = serializers.SlugRelatedField(
        slug_field='name',
        read_only=True,
    )

    class Meta:
        model = Review
        fields = '__all__'
        read_only_fields = ('title',)


class CommentSerializer(serializers.ModelSerializer):
    """
    Сериализатор модели Comment.
    """
    author = SlugRelatedField(
        slug_field='username',
        read_only=True
    )
    review = serializers.SlugRelatedField(
        slug_field='text',
        read_only=True
    )

    class Meta:
        model = Comment
        fields = '__all__'
        read_only_fields = ('review',)
