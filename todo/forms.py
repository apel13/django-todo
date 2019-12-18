from django import forms
from .models import Task


class TaskUpdateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'deadline', 'mark', 'status')


class TaskCreateForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = ('title', 'description', 'deadline', 'mark',)
