from .models import Activity
from django.contrib.contenttypes.models import ContentType

class ActivityCreateUpdateLogMixin:
    
    activity_action = 'updated' 

    def form_valid(self, form):
        response = super().form_valid(form)
        
        Activity.objects.create(
            user=self.request.user,
            action=self.activity_action,
            target=self.object
        )
        
        return response
    

class ActivityDeleteLogMixin:
    activity_action = 'deleted'

    def form_valid(self, form):
        
        content_type = ContentType.objects.get_for_model(self.object)
        
        # 2. Log the activity (Saving the Ghost Record)
        Activity.objects.create(
            user=self.request.user,
            action=self.activity_action,
            target_ct=content_type,     
            target_id=None, 
            target_deleted_name=str(self.object)             
        )
        
        # 3. Pass it down the chain to actually be deleted
        return super().form_valid(form)
    
