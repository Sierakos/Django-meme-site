from django.db.models.signals import post_save, pre_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender=User)
def create_profile(sender, instance, created, **kwargs):
    """
    Create profile when new user will create a new account
    """
    if created:
        Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_profile(sender, instance, **kwargs):
    """
    Save profile for every changes
    """
    instance.profile.save()

@receiver(pre_save, sender=Profile)
def pre_save_image(sender, instance, *args, **kwargs):
    """ 
    Every time user change profile file the previous
    one will be deleted.
    """
    old_img = instance.__class__.objects.get(id=instance.id).image.path
    try:
        new_img = instance.image.path
    except:
        new_img = None
    if new_img != old_img:
        import os
        if os.path.exists(old_img):
            os.remove(old_img)

