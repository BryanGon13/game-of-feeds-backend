from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User


class Profile(models.Model):
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=255, blank=True)
    bio = models.TextField(blank=True)
    profile_image = models.ImageField(
        upload_to='game_of_feeds/profile_images/', 
        default='game_of_feeds/default_profile_idzhze'
    )
    house = models.CharField(max_length=100, blank=True) # (Stark, Lannister etc...)
    followers = models.ManyToManyField(   # Social feature — tracks who follows this profile
        'self',
        symmetrical=False,
        related_name='following',
        blank=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']  # Newest profiles appear first

def __str__(self):
    return f"{self.owner}'s profile"

# This function will be called automatically after a User is saved
def create_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(owner=instance) # If the user is new, this will create a matching Profile and link it to that user (as 'owner')

post_save.connect(create_profile, sender=User) # Every time a User is saved, Django sends out a signal and this function listens for it