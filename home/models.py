from datetime import date
from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now



STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
    ]

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    due_date = models.DateField(default=now)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    reminder = models.BooleanField(default=False)
    is_archived = models.BooleanField(default=False)  # New field to archive tasks

    def save(self, *args, **kwargs):
        if self.status == 'completed':  
            self.is_archived = True  # Automatically archive if completed
        super().save(*args, **kwargs)

class SubTask(models.Model):
    task = models.ForeignKey(Task, related_name='subtasks', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)



