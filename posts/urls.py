from django.urls import path
from .views import PostListCreateAPIView, PostRetrieveUpdateDestroyAPIView, CommentListCreateAPIView

urlpatterns = [
    path('post/', PostListCreateAPIView.as_view(), name='post-list-create'),
    path('post/<int:pk>/', PostRetrieveUpdateDestroyAPIView.as_view(), name='post-detail'),
    path('post/<int:post_id>/comment/', CommentListCreateAPIView.as_view(), name='comment-list-create'),
]