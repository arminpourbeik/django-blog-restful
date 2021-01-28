import os

from imagekit.models import ImageSpecField
from pilkit.processors import ResizeToFill

from django.db import models
from django.utils import timezone
from django.conf import settings
from django.utils.timezone import now as timezone_now


class Category(models.Model):
    """
    Database model for category
    """

    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        verbose_name_plural = "categories"

    def __str__(self) -> str:
        return self.name


def upload_to(instance, filename):
    now = timezone_now()
    base, extention = os.path.splitext(filename)
    extention = extention.lower()

    return f"posts/{now:%Y/%m/%d}/{instance.pk}{extention}"


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
    created_at = models.DateTimeField(default=timezone.now, db_index=True)
    author = models.ForeignKey(
        to=settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="posts"
    )
    status = models.CharField(max_length=10, choices=OPTIONS, default="published")
    tags = models.ManyToManyField(to="Tag", related_name="posts", blank=True)
    header_picture = models.ImageField(upload_to=upload_to, blank=True, null=True)
    picture_large = ImageSpecField(
        source="header_picture",
        processors=[ResizeToFill(800, 400)],
        format="PNG",
    )
    picture_thumbnail = ImageSpecField(
        source="header_picture",
        processors=[ResizeToFill(728, 250)],
        format="PNG",
    )

    objects = models.Manager()  # Default manager
    published = PostObjects()  # Custom manager

    @property
    def num_of_comments(self):
        return self.comments.filter(active=True).count()

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


class Tag(models.Model):
    title = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.title