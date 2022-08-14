from datetime import datetime
from django.forms import ModelForm,ValidationError
from .models import *

class AssignmentsForm(ModelForm):
    class Meta:
        model=Assignments
        fields=['title','description','full_marks','deadline', 'is_scheduled', 'scheduled_time', 'course','file']
        
    def clean_scheduled_time(self):
        scheduled_time=self.cleaned_data['scheduled_time']
        if scheduled_time:
            if scheduled_time.timestamp() <= datetime.now().timestamp():
                raise ValidationError(
                    "Schedule time should be ahead of present time"
                )
            return scheduled_time
    
    def clean_deadline(self):
        deadline=self.cleaned_data['deadline']
        if deadline:
            if deadline.timestamp() <= datetime.now().timestamp():
                raise ValidationError(
                    "Deadline should be ahead of present time"
                )
            return deadline
    
    def clean(self):
        cleaned_data = super().clean()
        scheduled_time = cleaned_data.get('scheduled_time')
        deadline = cleaned_data.get('deadline')
        if scheduled_time and deadline:
            if scheduled_time.timestamp() >= deadline.timestamp():
                self.add_error('deadline', "Deadline should be ahead of schedule time")
        return cleaned_data        