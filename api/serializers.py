from django.db.models import fields
from rest_framework import serializers

from blog.models import Post, Comment, Category


class PostSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Post
        fields = (
            "pk",
            "url",
            "title",
            "excerpt",
            "content",
            "created_at",
            "status",
        )
        extra_kwargs = {
            "created_at": {"write_only": True},
            "status": {"write_only": True},
        }


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Category
        fields = (
            "pk",
            "url",
            "name",
        )


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Comment
        fields = (
            "url",
            "pk",
            "body",
            "created_at",
        )
        extra_kwargs = {
            "created_at": {"write_only": True},
        }