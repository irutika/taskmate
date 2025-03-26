from django import forms
from .models import Task
from .models import SubTask

class TaskForm(forms.ModelForm):
    class Meta:
        model = Task
        fields = [
            'title',          # Task title
            'description',    # Task description
            'due_date',       # Due date for the task
            'status',         # Status of the task (e.g., Pending, Completed)
            'reminder',       # Field for setting a reminder
        ]

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter task title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter task description'}),
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'reminder': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

class SubTaskForm(forms.ModelForm):
    class Meta:
        model = SubTask
        fields = [
            'task',           # Foreign key to the main task
            'title',          # Subtask title
        ]

