from django import forms
from tasks.models import Task


class AddTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'deadline')
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'deadline':"Дэдлайн (не обяз.)"
        }

class EditTaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('name', 'description', 'deadline', 'status', 'user')
        widgets = {
            'deadline': forms.DateInput(attrs={'type': 'datetime-local'}),
        }
        labels = {
            'deadline': "Дэдлайн (не обяз.)"
        }