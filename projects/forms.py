from django import forms
from tasks.models import Task

class FilterTaskType(forms.Form):
    status_task_type = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=Task.STATUS_CHOICES,
        required=False
    )
    priority_task_type = forms.MultipleChoiceField(
        widget=forms.CheckboxSelectMultiple,
        choices=Task.PRIORITY_CHOICES,
        required=False
    )