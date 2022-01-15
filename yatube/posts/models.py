from django.db import models
from django.contrib.auth import get_user_model

from .validators import validate_not_empty


User = get_user_model()


class Group(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    description = models.TextField()

    def __str__(self) -> str:
        return self.title


class Post(models.Model):
    text = models.TextField(
        validators=[validate_not_empty], verbose_name="Текст поста"
    )

    pub_date = models.DateTimeField(auto_now_add=True)

    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )

    group = models.ForeignKey(
        Group,
        on_delete=models.SET_NULL,
        related_name="posts",
        blank=True,
        null=True,
        verbose_name="Группа поста",
    )

    class Meta:
        ordering = ["-pub_date"]

    def __str__(self) -> str:
        return self.text[:15]
