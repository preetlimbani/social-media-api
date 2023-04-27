from django.urls import path
from .views import (
    AuthenticateAPIView, FollowAPIView, UnfollowAPIView, UserAPIView, PostAPIView,
    DeletePostAPIView, LikeAPIView, UnlikeAPIView, CommentAPIView, SinglePostAPIView,
    AllPostsAPIView, CreateUserRegistration
)

urlpatterns = [
    path('register/', CreateUserRegistration.as_view(), name='authenticate'),
    path('authenticate/', AuthenticateAPIView.as_view(), name='authenticate'),
    path('follow/<int:id>/', FollowAPIView.as_view(), name='follow'),
    path('unfollow/<int:id>/', UnfollowAPIView.as_view(), name='unfollow'),
    path('user/', UserAPIView.as_view(), name='user'),
    path('posts/', PostAPIView.as_view(), name='post'),
    path('posts/<int:id>/', DeletePostAPIView.as_view(), name='delete_post'),
    path('like/<int:id>/', LikeAPIView.as_view(), name='like'),
    path('unlike/<int:id>/', UnlikeAPIView.as_view(), name='unlike'),
    path('comment/<int:id>/', CommentAPIView.as_view(), name='comment'),
    path('posts/<int:id>/', SinglePostAPIView.as_view(), name='single_post'),
    path('all_posts/', AllPostsAPIView.as_view(), name='all_posts'),
    ]
