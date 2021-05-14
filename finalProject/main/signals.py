from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from main.models import Card


@receiver(post_save, sender=Card)
def credit_card_created(sender, instance, created, **kwargs):
    if created:
        print(f'New credit card is added, ID: {instance}')