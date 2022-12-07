from django.contrib.auth.decorators import login_required
from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import viewsets
from beers.filters import ReviewFilter, CommentFilter, BeerFilter
from beers.models import Beer, Review, Comment, Category
from beers.permissions import AuthorPermission
from beers.serializers import BeerSerializer, ReviewSerializer, CommentSerializer, CategorySerializer
from django_filters import rest_framework as filters


@api_view(['GET'])
def api_overview(request):
    api = {}
    return Response(api)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

    def get_permissions(self):
        if self.request.method in ['GET', ]:
            return [permissions.IsAuthenticated(), ]
        return [permissions.IsAdminUser(), ]


class BeerViewSet(viewsets.ModelViewSet):
    queryset = Beer.objects.filter(active=True)
    serializer_class = BeerSerializer
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = BeerFilter

    def get_permissions(self):
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
        if self.request.method in ['GET', 'POST']:
            return [permissions.IsAuthenticated(), ]
        elif self.request.method in ['PUT', 'DELETE']:
            return [AuthorPermission(), ]
        return [permissions.IsAdminUser(), ]

# @api_view(['GET', 'POST'])
# def beers_list(request):
#     if request.method == 'GET':
#         beers = Beer.objects.filter()
#         serializer = BeerSerializer(beers, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = BeerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def beer_detail(request, beer_pk):
#     try:
#         beer = Beer.objects.get(pk=beer_pk)
#     except Beer.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = BeerSerializer(beer)
#         return Response(serializer.data)
#
#     elif request.method == 'PUT':
#         serializer = BeerSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         beer.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(['GET', 'POST'])
# def reviews_list(request):
#     if request.method == 'GET':
#         reviews = ReviewFilter(request.GET, queryset=Review.objects.all()).qs
#         serializer = ReviewSerializer(reviews, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def review_details(request, review_pk):
#     try:
#         review = Review.objects.get(pk=review_pk)
#     except Beer.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     except Review.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = ReviewSerializer(review)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = ReviewSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         review.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(['GET', 'POST'])
# def comments_list(request):
#     if request.method == 'GET':
#         comments = CommentFilter(request.GET, queryset=Comment.objects.all()).qs
#         serializer = CommentSerializer(comments, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def comment_detail(request, comment_pk):
#     try:
#         comment = Comment.objects.get(pk=comment_pk)
#     except Comment.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#
#     if request.method == 'GET':
#         serializer = CommentSerializer(comment)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         serializer = CommentSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#     elif request.method == 'DELETE':
#         comment.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#
#
# @api_view(["GET", "POST"])
# def categories_list(request):
#     if request.method == 'GET':
#         categories = Category.objects.all()
#         serializer = CategorySerializer(categories, many=True)
#         return Response(serializer.data)
#     elif request.method == 'POST':
#         serializer = CategorySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#
# @api_view(['GET', 'PUT', 'DELETE'])
# def category_details(request, category_pk):
#     try:
#         category = Category.objects.get(pk=category_pk)
#     except Category.DoesNotExist:
#         return Response(status=status.HTTP_404_NOT_FOUND)
#     if request.method == 'GET':
#         serializer = CategorySerializer(category)
#         return Response(serializer.data)
#     elif request.method == 'PUT':
#         pass
#     elif request.method == 'DELETE':
#         pass
