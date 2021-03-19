from django.db import models


class Page(models.Model):
    url = models.CharField(
        max_length=100,
        unique=True,
    )
    title = models.CharField(max_length=100)
    content = models.TextField(blank=True)

    def __str__(self):
        return f"{self.url}: {self.title}"
