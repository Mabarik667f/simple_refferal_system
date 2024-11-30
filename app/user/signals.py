import random
from string import ascii_letters, digits
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from user.models import InvitationCode


@receiver(post_save, sender=Token)
def create_invitate_code_for_user(sender, instance, created, **kwargs):
    if created:
        code = "".join(random.choices(ascii_letters+digits, k=6))
        InvitationCode.objects.create(
            user=instance.user,
            code=code
        )
