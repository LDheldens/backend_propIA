from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import ImageProperty

@receiver(post_delete, sender=ImageProperty)
def delete_image_file(sender, instance, **kwargs):
    if instance.image:
        instance.image.delete(False)
