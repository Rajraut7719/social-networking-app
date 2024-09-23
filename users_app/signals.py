from django.dispatch import receiver
from django.db.models.signals import post_save
from users_app.models import User
from rest_framework.authtoken.models import Token


@receiver(post_save, sender=User)
def basic_account_setting_create(sender, instance, created, **kwargs):
    try:
        if created:
            Token.objects.create(user=instance)
    except Exception:
        pass
