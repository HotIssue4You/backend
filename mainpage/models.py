from django.db import models

# Create your models here.
class Article(models.Model):
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField # (auto_now_add=True)
    link_url = models.URLField(max_length=200)
    
class WordCloud(models.Model):
    image_url = models.URLField(max_length=200)
    # 여기도 시간대가 있어야하지 않을까?
    created_at = models.DateTimeField
    
