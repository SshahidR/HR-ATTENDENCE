from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser

@receiver(post_save, sender=User)
def update_customer_status(sender, instance, **kwargs):
    try:
        customer = CustomUser.objects.get(email_address=instance.email)
    except CustomUser.DoesNotExist:
        # Customer object not found, create it
        customer = CustomUser.objects.create(
            name=instance.first_name + ' ' + instance.last_name,
            email_address=instance.email
        )

    # Update the status field based on is_active field of User
    if instance.is_active:
        customer.status = 'active'
    else:
        customer.status = 'inactive'
    customer.save()
    

from .models import *
from django.db.models.signals import post_save
from django.dispatch import receiver
@receiver(post_save, sender=MasterTable)
def update_related_models(sender, instance, **kwargs):
    if instance.user:
        visitingCard.objects.update_or_create(
            user=instance.user,
            defaults={
                'username': getattr(instance, 'username', ''),
                'mobilenum': getattr(instance, 'mobilenum', ''),
                'email': getattr(instance, 'email', ''),
                'poBox': getattr(instance, 'poBox', ''),
                'unitedstate': getattr(instance, 'unitedstate', ''),
                'designation': getattr(instance, 'designation', ''),
                'country': getattr(instance, 'country', ''),
                'telphone': getattr(instance, 'telphone', ''),
                'extnum': getattr(instance, 'extnum', ''),
                'faxnum': getattr(instance, 'faxnum', ''),
            }
        )
        userAttendance.objects.update_or_create(
            user=instance.user,
            defaults={
                'check_in': getattr(instance, 'check_in', None),
                'check_out': getattr(instance, 'check_out', None),
                'status': getattr(instance, 'status', ''),
                'total_hours': getattr(instance, 'total_hours', ''),
                'working_hours': getattr(instance, 'working_hours', ''),
                'username': getattr(instance, 'username', ''),
                'chk_date': getattr(instance, 'chk_date', None),
            }
        )
        daywiseAttendance.objects.update_or_create(
            user=instance.user,
            defaults={
                'check_in': getattr(instance, 'check_in', None),
                'check_out': getattr(instance, 'check_out', None),
                'status': getattr(instance, 'status', ''),
                'timeShortageExceed': getattr(instance, 'timeShortageExceed', ''),
                'total_hours': getattr(instance, 'total_hours', ''),
                'username': getattr(instance, 'username', ''),
                'chk_date': getattr(instance, 'chk_date', None),
            }
        )
