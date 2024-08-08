from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


def article_preview_directory_path(instance: "Article", filename: str):
    return "articles/article_{id}/preview/{filename}".format(
        id=instance.id,
        filename=filename
    )


class Article(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    published_at = models.DateTimeField(auto_now_add=True)
    published_by = models.ForeignKey(User, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=50, null=True, blank=True)
    preview_img = models.ImageField(null=True, blank=True, upload_to=article_preview_directory_path)
    likes = models.ManyToManyField(User, related_name='liked_articles', blank=True)

    def number_of_likes(self):
        return self.likes.count()

    def get_absolute_url(self):
        return reverse('newsfeed:article-detail', kwargs={'pk': self.pk})

    def __str__(self):
        return f"article: {self.title}, author: {self.author_name}"

    def save(self, *args, **kwargs):
        if not self.author_name and self.published_by:
            self.author_name = self.published_by.username
        super(Article, self).save(*args, **kwargs)

    class Meta:
        ordering = ['-published_at']

