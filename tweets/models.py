import random
from django.conf import settings

from django.db import models

User = settings.AUTH_USER_MODEL

class TweetLike(models.Model):
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    tweet = models.ForeignKey("Tweet", on_delete= models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

class Tweet(models.Model):
    # id = models.AutoField(PRIMARY_KEY=True) Automaticaly added by django
    parent = models.ForeignKey("self", null=True, on_delete=models.SET_NULL)
    user = models.ForeignKey(User, on_delete= models.CASCADE)
    content = models.TextField(blank=True, null=True) # null for DB, blank for django
    likes = models.ManyToManyField(User, related_name='tweet_user', blank=True, through=TweetLike)
    image = models.FileField(upload_to='images/', blank=True, null=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-id']
        
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 299)
            }
        
    