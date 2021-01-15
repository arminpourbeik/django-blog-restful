from django.db import models
from django.utils import timezone
from django.conf import settings


class Category(models.Model):
    """
    Database model for category
    """

    name = models.CharField(max_length=100, unique=True)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name


class Post(models.Model):
    """
    Database model for post
    """

    class PostObjects(models.Manager):
        def get_queryset(self):
            return super().get_queryset().filter(status="published")

    OPTIONS = (
        ("draft", "Draft"),
        ("published", "Published"),
    )
    title = models.CharField(max_length=250)
    excerpt = models.TextField(null=True)
    category = models.ForeignKey(
        to=Category, on_delete=models.PROTECT, related_name="posts"
    )
    content = models.TextField()
    slug = models.SlugField(max_length=255, unique_for_date="created_at")
    created_at = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    status = models.CharField(max_length=10, choices=OPTIONS, default="published")

    objects = models.Manager()  # Default manager
    published = PostObjects()  # Custom manager

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.title


class Comment(models.Model):
    """
    Database model for comments
    """

    body = models.TextField(max_length=500)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(to=Post, on_delete=models.CASCADE, related_name="comments")
    created_at = models.DateTimeField(default=timezone.now)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return "{} - by {}".format(self.body[:10], self.author.username)
