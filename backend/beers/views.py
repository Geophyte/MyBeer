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
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated(), ]


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        # return [permissions.AllowAny(),]
        if self.request.method in ['GET']:
            return [permissions.IsAuthenticated(), ]
        return [permissions.IsAdminUser(), ]


class BeerViewSet(viewsets.ModelViewSet):
    queryset = Beer.objects.filter()
    serializer_class = BeerSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BeerFilter

    def get_serializer_class(self):
        if self.request.method in ['GET']:
            return BeerReadSerializer
        return BeerSerializer

    def get_permissions(self):
        # return [permissions.AllowAny(),]
        if self.request.method in ['GET', 'POST']:
            return [permissions.IsAuthenticated(), ]
        elif self.request.method in ['PUT', 'DELETE']:
            return [permissions.IsAdminUser(), ]
        return [permissions.IsAdminUser(), ]


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.filter()
    serializer_class = ReviewSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = ReviewFilter

    def get_permissions(self):
        # return [permissions.AllowAny(),]
        if self.request.method in ['GET', 'POST']:
            return [permissions.IsAuthenticated(), ]
        elif self.request.method in ['PUT', 'DELETE']:
            return [AuthorPermission(), ]
        return [permissions.IsAdminUser(), ]


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = CommentFilter

    def get_permissions(self):
        # return [permissions.AllowAny(),]
        if self.request.method in ['GET', 'POST']:
            return [permissions.IsAuthenticated(), ]
        elif self.request.method in ['PUT', 'DELETE']:
            return [AuthorPermission(), ]
        return [permissions.IsAdminUser(), ]
