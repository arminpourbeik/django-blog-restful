from django.db.models import Count
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.reverse import reverse
from rest_framework import permissions
from rest_framework.parsers import MultiPartParser, FormParser

from blog.models import Category, Post, Comment
from api.custompermissions import IsCurrentUserAuthorOrReadOnly
from api.serializers import PostSerializer, CategorySerializer, CommentSerializer
from api.filters import PostFilter, CategoryFilter, CommentFilter
from utils.renderers import BlogRenderers


class PostListView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    queryset = Post.published.all()
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = PostFilter
    ordering_fields = ("created_at",)
    renderer_classes = (BlogRenderers,)
    parser_classes = [MultiPartParser, FormParser]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.published.all()
    permission_classes = (IsCurrentUserAuthorOrReadOnly,)
    renderer_classes = (BlogRenderers,)


class CategoryListView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    filter_class = CategoryFilter
    renderer_classes = (BlogRenderers,)


class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()
    renderer_classes = (BlogRenderers,)


class CommentListView(generics.ListAPIView):
    serializer_class = CommentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    filter_class = CommentFilter
    renderer_classes = (BlogRenderers,)

    def get_queryset(self):
        return Comment.objects.filter(active=True)


class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (IsCurrentUserAuthorOrReadOnly,)
    renderer_classes = (BlogRenderers,)


class CreatePostCommentView(generics.CreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = (permissions.IsAuthenticated,)
    renderer_classes = (BlogRenderers,)

    def perform_create(self, serializer):
        post_id = self.kwargs.get("pk")
        serializer.save(author=self.request.user, post_id=post_id)


class GetMostCommentedPosts(generics.GenericAPIView):
    """
    View for getting most commented posts
    """

    renderer_classes = (BlogRenderers,)

    def get(self, request, *args, **kwargs):
        count = self.kwargs.get("count", 5)
        most_commented_posts = Post.published.annotate(
            total_comments=Count("comments")
        ).order_by("-total_comments")[:count]

        serializer = PostSerializer(
            most_commented_posts, many=True, context={"request": request}
        )
        data = serializer.data

        return Response({"posts": data})


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