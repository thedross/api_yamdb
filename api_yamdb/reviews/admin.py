from django.contrib import admin
from django.contrib.auth.models import Group

from .models import Category, Comment, Genre, Review, Title

admin.site.unregister(Group)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', )
    empty_value_display = '-пусто-'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('review', 'author', 'text')
    search_fields = ('text', )
    list_filter = ('review', 'author')
    empty_value_display = '-пусто-'


@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name', )
    empty_value_display = '-пусто-'


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'text', 'score')
    search_fields = ('text', )
    list_filter = ('title', 'author',)
    empty_value_display = '-поставьте оценку-'


@admin.register(Title)
class TitleAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'category', 'genres')
    search_fields = ('name', )
    list_filter = ('category', )
    empty_value_display = '-пусто-'

    def genres(self, obj):
        return [genre.name for genre in obj.genre.all()]
