from django_filters.rest_framework import CharFilter, NumberFilter, FilterSet
from titles.models import Title


class TitleFilterSet(FilterSet):
    """Фильрт-сет для вью TitleViewSet."""
    name = CharFilter(field_name='name')
    year = NumberFilter(field_name='year')
    genre = CharFilter(field_name='genre__slug')
    category = CharFilter(field_name='category__slug')

    class Meta:
        model = Title
        fields = ('name', 'year', 'genre', 'category')
