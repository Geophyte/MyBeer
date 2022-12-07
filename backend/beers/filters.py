from django_filters import rest_framework as filters
from .models import Beer, Review, Comment


class ReviewFilter(filters.FilterSet):
    """
    http://127.0.0.1:8000/api/v1/comments/?beer=1
    """

    beer = filters.NumberFilter(field_name='beer')

    class Meta:
        model = Review
        fields = ('beer',)


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
