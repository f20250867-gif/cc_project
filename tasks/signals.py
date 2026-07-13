# from django.db.models.signals import post_save
# from django.contrib.auth.models import User
# from django.dispatch import receiver   
# from activity.models import Activity
# from .models import Task

# @receiver(post_save, sender=Task)
# def log_task_creation(sender, instance, created, **kwargs):
#     if created:
#         Activity.objects.create(
#             user=instance.created_by,
#             action='created',
#             target=instance,
#         )
        
