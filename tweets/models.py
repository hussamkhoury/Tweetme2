import random
from django.db import models

class Tweet(models.Model):
    # id = models.AutoField(PRIMARY_KEY=True) Automaticaly added by django
    content = models.TextField(blank=True, null=True) # null for DB, blank for django
    image = models.FileField(upload_to='images/', blank=True, null=True)
    class Meta:
        ordering = ['-id']
        
    def serialize(self):
        return {
            "id": self.id,
            "content": self.content,
            "likes": random.randint(0, 299)
            }
        
    