from rest_framework import generics

from blog.models import Category, Post, Comment
from api.serializers import PostSerializer, CategorySerializer, CommentSerializer


class PostListView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.published.all()


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
    queryset = Comment.objects.all()


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()