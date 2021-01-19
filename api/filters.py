from django_filters import rest_framework as filters
from django_filters import AllValuesFilter, CharFilter, NumberFilter

from blog.models import Post, Category, Comment


class PostFilter(filters.FilterSet):
    class Meta:
        model = Post
        fields = (
            "title",
            "category_name",
            "release_year",
            "release_month",
            "release_day",
            "author_name",
        )

    author_name = AllValuesFilter(field_name="author__username")
    category_name = AllValuesFilter(field_name="category__name")
    title = CharFilter(lookup_expr="icontains")
    release_year = NumberFilter(field_name="created_at", lookup_expr="year")
    release_month = NumberFilter(field_name="created_at", lookup_expr="month")
    release_day = NumberFilter(field_name="created_at", lookup_expr="day")


class CategoryFilter(filters.FilterSet):
    class Meta:
        model = Category
        fields = ("name",)

    name = CharFilter(lookup_expr="icontains")


class CommentFilter(filters.FilterSet):
    class Meta:
        model = Comment
        fields = (
            "author",
            "release_year",
            "release_month",
            "release_day",
        )

    release_year = NumberFilter(field_name="created_at", lookup_expr="year")
    release_month = NumberFilter(field_name="created_at", lookup_expr="month")
    release_day = NumberFilter(field_name="created_at", lookup_expr="day")
