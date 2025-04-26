from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class UserProfile(models.Model):
    """
    User profile model that extends the built-in Django User model.
    Stores additional user information and preferences.
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    
    # User preferences
    default_chart_type = models.CharField(
        max_length=20,
        choices=[
            ('bar', 'Bar Chart'),
            ('line', 'Line Chart'),
            ('pie', 'Pie Chart'),
            ('scatter', 'Scatter Plot'),
        ],
        default='bar'
    )
    
    default_color_scheme = models.CharField(
        max_length=20,
        choices=[
            ('default', 'Default'),
            ('pastel', 'Pastel'),
            ('vibrant', 'Vibrant'),
            ('monochrome', 'Monochrome'),
        ],
        default='default'
    )
    
    show_data_tooltips = models.BooleanField(default=True)
    enable_email_notifications = models.BooleanField(default=False)
    
    # Date and time fields
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s profile"


# Signal to create or update user profile when user is created or updated
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to create or update user profile when user is created or updated.
    """
    if created:
        UserProfile.objects.create(user=instance)
    else:
        instance.profile.save()