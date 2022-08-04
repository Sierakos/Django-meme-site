from django.db.models.signals import post_delete
from .models import Post
from django.dispatch import receiver

@receiver(post_delete, sender=Post)
def delete_post_image(sender, instance, *args, **kwargs):
    """
    Delete image from media when somebody delete post
    """
    old_img = instance.image.path
    import os
    if os.path.isfile(old_img):
        os.remove(old_img)