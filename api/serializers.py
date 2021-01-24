from rest_framework import serializers

from blog.models import Post, Comment, Category, Tag


class PostTagsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ("title",)

    def to_representation(self, instance):
        return instance.title

    def to_internal_value(self, data):
        return self.Meta.model.objects.get_or_create(title=data)


class PostSerializer(serializers.HyperlinkedModelSerializer):
    author = serializers.ReadOnlyField(source="author.username")
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(), slug_field="name"
    )
    tags = PostTagsSerializer(many=True, required=False)

    def create(self, validated_data):
        tags = validated_data.pop("tags", None)

        new_post = self.Meta.model.objects.create(**validated_data)
        if tags:
            for tag in tags:
                tag[0].posts.add(new_post)

        return new_post

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
            "tags",
            "num_of_comments",
        )
        extra_kwargs = {
            "created_at": {"read_only": True},
            "status": {"read_only": True},
            "num_of_comments": {"read_only": True},
        }


class CategorySerializer(serializers.HyperlinkedModelSerializer):
    posts = serializers.HyperlinkedRelatedField(
        many=True, read_only=True, view_name="post-detail"
    )

    class Meta:
        model = Category
        fields = (
            "pk",
            "url",
            "name",
            "posts",
        )


class CommentSerializer(serializers.HyperlinkedModelSerializer):
    post = serializers.HyperlinkedRelatedField(read_only=True, view_name="post-detail")
    author = serializers.ReadOnlyField(source="author.username")

    class Meta:
        model = Comment
        fields = (
            "url",
            "pk",
            "body",
            "created_at",
            "post",
            "author",
        )
        extra_kwargs = {
            "created_at": {"read_only": True},
        }
