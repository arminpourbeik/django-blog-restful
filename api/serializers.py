from rest_framework import serializers

from blog.models import Post, Comment, Category


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="name"
    )

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
            "author",
            "category",
        )
        extra_kwargs = {
            "created_at": {"read_only": True},
            "status": {"read_only": True},
        }


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="post-detail"
    )

    class Meta:
        model = Category
        fields = ("pk", "url", "name", "posts")


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    post = serializers.HyperlinkedRelatedField(read_only=True, view_name="post-detail")

    class Meta:
        model = Comment
        fields = (
            "url",
            "pk",
            "body",
            "created_at",
            "post",
        )
        extra_kwargs = {
            "created_at": {"read_only": True},
        }