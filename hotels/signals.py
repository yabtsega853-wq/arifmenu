from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User


@receiver(post_save, sender=User)
def create_hotel_profile(sender, instance, created, **kwargs):
    if created:
        # Import inside the function to avoid circular import
        from .models import Hotel
        if not hasattr(instance, 'hotel'):
            Hotel.objects.create(owner=instance, name=instance.username)
