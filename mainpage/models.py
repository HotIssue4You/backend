from django.db import models

# Create your models here.
class Article(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    link_url = models.URLField(max_length=200)
    
class WordCloud(models.Model):
    # id = 
    image_url = models.URLField(max_length=200)