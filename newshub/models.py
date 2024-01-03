from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Comments(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='comments')
    text = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    news_id = models.CharField(max_length=500)
    is_delete= models.BooleanField(default=False,null=True,blank=True)

    class Meta:
        db_table = 'comments'
        indexes = [
            models.Index(fields=[ 'news_id','is_delete']),
        ]

class Reactions(models.Model):
    user_id = models.ForeignKey(User,on_delete=models.CASCADE,null=True,blank=True,related_name='reactions')
    reaction_type = models.TextField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    news_id = models.CharField(max_length=500)
    is_delete= models.BooleanField(default=False,null=True,blank=True)

    class Meta:
        db_table = 'reactions'
        indexes = [
            models.Index(fields=[ 'news_id','is_delete']),
        ]
