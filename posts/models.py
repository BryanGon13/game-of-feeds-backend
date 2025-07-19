from django.db import models
from django.contrib.auth.models import User


# Create your models here.

class Post(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    image = models.ImageField(
        upload_to='game_of_feeds/post_images/', 
        default='game_of_feeds/default_post_ysiykv', 
        blank=False, 
        null=False
    )
    caption = models.TextField(blank=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Post by {self.owner.username} at {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"