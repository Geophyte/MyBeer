from django.urls import path, include
from rest_framework import routers

from beers import views
from beers.views import CategoryViewSet, BeerViewSet, CommentViewSet, ReviewViewSet, UserViewSet

router = routers.DefaultRouter()
router.register('categories', CategoryViewSet)
router.register('beers', BeerViewSet)
router.register('reviews', ReviewViewSet)
router.register('comments', CommentViewSet)
router.register('users', UserViewSet)
urlpatterns = [
    path('', include(router.urls)),
]
