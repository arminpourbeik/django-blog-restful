from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse

from blog.models import Category, Post, Comment
from api.serializers import PostSerializer, CategorySerializer, CommentSerializer


class PostListView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.published.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.published.all()


class CategoryListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer

    def get_queryset(self):
        return Comment.objects.filter(active=True)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()


class CreatePostCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()

    def perform_create(self, serializer):
        post_id = self.kwargs.get("pk")
        serializer.save(author=self.request.user, post_id=post_id)


class ApiRoot(generics.GenericAPIView):
    """
    API root for django blog API
    """

    def get(self, request, *args, **kwargs):
        return Response(
            {
                "posts": reverse("post-list", request=request),
                "categories": reverse("category-list", request=request),
                "comments": reverse("comment-list", request=request),
            }
        )