from django.db import models

# Create your models here.
class Tag(models.Model):
    tag = models.CharField(max_length = 32,unique=True)  
    
class Article(models.Model):
    header = models.CharField(max_length = 64,unique=True)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)
    
