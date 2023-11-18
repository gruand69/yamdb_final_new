# from django.urls import include, path

# from .views import create_token, CreateUserView

# urlpatterns = [
# #    path('auth/signup/', create_user),
#     path('auth/signup/', CreateUserView.as_view()),
#     path('auth/token/', create_token)
# ]
# ----------------------------------------------------------
from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet, create_user,
                    get_token)

router = DefaultRouter()
router.register('users', UserViewSet, basename='user')
router.register('titles', TitleViewSet)
router.register('categories', CategoryViewSet)
router.register('genres', GenreViewSet)
router.register(r'titles/(?P<title_id>\d+)/reviews', ReviewViewSet,
                basename='reviews')
router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet, basename='reviews')

urlpatterns = [
    path('auth/signup/', create_user, name='create_user'),
    path('auth/token/', get_token, name='get_token'),
    path('', include(router.urls)),
]
