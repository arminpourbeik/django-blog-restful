from django.urls import path

from . import views

urlpatterns = [
    path("", views.PostListView.as_view(), name="post-list"),
    path("<int:pk>/", views.PostDetailView.as_view(), name="post-detail"),
    path("categories/", views.CategoryListView.as_view(), name="category-list"),
    path(
        "categories/<int:pk>/",
        views.CategoryDetailView.as_view(),
        name="category-detail",
    ),
    path("comments/", views.CommentListView.as_view(), name="comment-list"),
    path(
        "comments/<int:pk>/", views.CommentDetailView.as_view(), name="comment-detail"
    ),
]
