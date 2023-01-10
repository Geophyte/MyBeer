from django.contrib.auth.models import User
from rest_framework import permissions, mixins
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import viewsets
from beers.filters import ReviewFilter, CommentFilter, BeerFilter
from beers.models import Beer, Review, Comment, Category
from beers.permissions import AuthorPermission
from beers.serializers import BeerSerializer, BeerReadSerializer, ReviewSerializer, CommentSerializer, \
    CategorySerializer
from django_filters import rest_framework as filters
from users.serializers import UserSerializer


@api_view(['GET'])
def api_overview(request):
    api = {}
    return Response(api)


class UserViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):
    """
    users/<int:id>/
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated(), ]


class CategoryViewSet(viewsets.ModelViewSet):
    """
    categories/
    categories/<int:id>/
    """
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in ['GET']:
            return [permissions.IsAuthenticated(), ]
        return [permissions.IsAdminUser(), ]


class BeerViewSet(viewsets.ModelViewSet):
    """
    beers/
    beers/<int:id>/
    beers/?category=<str:category>
    beers/?name=<str:name>
    """
    serializer_class = BeerSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BeerFilter

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return BeerReadSerializer
        return BeerSerializer

    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            return [permissions.IsAuthenticated(), ]
        return [permissions.IsAdminUser(), ]

    def get_queryset(self):
        if self.request.method in ['GET', ]:
            return Beer.objects.filter(active=True)
        else:
            return Beer.objects.all()


class ReviewViewSet(viewsets.ModelViewSet):
    """
    reviews/
    reviews/<int:id>/
    reviews/beer_name=
    reviews/beer_id=
    """
    serializer_class = ReviewSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ReviewFilter

    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            return [permissions.IsAuthenticated(), ]
        elif self.request.method in ['PATCH', 'DELETE']:
            return [AuthorPermission(), ]
        return [permissions.IsAdminUser(), ]

    def get_queryset(self):
        if self.request.method in ['GET', ]:
            return Review.objects.filter(active=True, beer__active=True)
        else:
            return Review.objects.all()


class CommentViewSet(viewsets.ModelViewSet):
    """
    comments/
    comments/<int:id>/
    comment/?review=
    """

    serializer_class = CommentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CommentFilter

    def get_permissions(self):
        if self.request.method in ['GET', 'POST']:
            return [permissions.IsAuthenticated(), ]
        elif self.request.method in ['PATCH', 'DELETE']:
            return [AuthorPermission(), ]
        return [permissions.IsAdminUser(), ]

    def get_queryset(self):
        if self.request.method in ['GET', ]:
            return Comment.objects.filter(active=True, review__active=True, review__beer__active=True)
        else:
            return Comment.objects.all()
