from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.TextField()
    noun_title = models.TextField(null=True)
    created_at = models.DateTimeField()