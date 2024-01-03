from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=255,null=True,blank=True)
    content = models.TextField(null=True,blank=True)
    source_url = models.CharField(max_length=1000,null=True,blank=True)
    publishedAt = models.DateTimeField(auto_now_add=True)
    author = models.CharField(max_length=200,null=True,blank=True)
    description = models.TextField(null=True,blank=True)
    source = models.CharField(max_length=255,null=True,blank=True)
    urlToImage= models.CharField(max_length=1000,null=True,blank=True)
    category=models.CharField(max_length=255,null=True,blank=True)

    class Meta:
        managed=False
        abstract=True