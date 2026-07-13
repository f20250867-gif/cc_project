from django.db import models
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

class Activity(models.Model):
    user = models.ForeignKey(User,related_name='user',on_delete=models.CASCADE)
    action = models.CharField(max_length=255)
    target_ct = models.ForeignKey(ContentType, blank=True, null=True, related_name='target_obj', on_delete=models.CASCADE)
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_ct', 'target_id')
    created_at = models.DateTimeField(auto_now_add=True)
    target_deleted_name = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        ordering = ('-created_at',)

    def __str__(self):
        if self.target:
            return f"{self.user.username} {self.action} {self.target}"
        else:
            return f"{self.user.username} {self.action} {self.target_deleted_name}"
    
