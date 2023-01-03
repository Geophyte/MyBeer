from django_filters import rest_framework as filters
from .models import Beer, Review, Comment


class ReviewFilter(filters.FilterSet):
    """
    http://127.0.0.1:8000/api/v1/reviews/?beer=1
    """

    beer_name = filters.CharFilter(field_name='beer__name', lookup_expr='exact')
    beer_id = filters.NumberFilter(field_name='beer_id')

    class Meta:
        model = Review
        fields = ('beer_name', 'beer_id')


class CommentFilter(filters.FilterSet):
    """
    http://127.0.0.1:8000/api/v1/comments/?review=15
    """
    review = filters.NumberFilter(field_name='review')

    class Meta:
        model = Comment
        fields = ('review',)


class BeerFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__name', lookup_expr='exact')

    class Meta:
        model = Beer
        fields = ('category',)
