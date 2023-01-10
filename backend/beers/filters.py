from django_filters import rest_framework as filters
from .models import Beer, Review, Comment


class ReviewFilter(filters.FilterSet):
    beer_name = filters.CharFilter(field_name='beer__name', lookup_expr='exact')
    beer_id = filters.NumberFilter(field_name='beer_id')

    class Meta:
        model = Review
        fields = ('beer_name', 'beer_id')


class CommentFilter(filters.FilterSet):
    review = filters.NumberFilter(field_name='review')

    class Meta:
        model = Comment
        fields = ('review',)


class BeerFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__name', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Beer
        fields = ('category', 'name')
