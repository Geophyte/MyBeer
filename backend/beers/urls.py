from django.urls import path, include
from rest_framework import routers
from beers.views import CategoryViewSet, BeerViewSet, CommentViewSet, ReviewViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet, basename='Category')
router.register('beers', BeerViewSet, basename='Beer')
router.register('reviews', ReviewViewSet, basename='Review')
router.register('comments', CommentViewSet, basename='Comment')
router.register('users', UserViewSet, basename='User')
urlpatterns = [
    path('', include(router.urls)),
]
