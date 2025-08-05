import uuid

from django.db import models
from django.forms import ModelForm


class Board(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(blank=False, null=False, max_length=64)
    description = models.TextField(blank=True, null=False, default="", max_length=512)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TaskState(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=64)
    description = models.TextField(blank=True, null=False, default="", max_length=512)
    index = models.PositiveIntegerField(blank=False, null=False, default=0)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_state = models.ForeignKey(TaskState, on_delete=models.CASCADE)
    name = models.CharField(blank=False, null=False, max_length=64)
    description = models.TextField(blank=True, null=False, default="", max_length=512)
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class BoardForm(ModelForm):
    class Meta:
        model = Board
        exclude = ['id', 'created_datetime']


class TaskForm(ModelForm):
    class Meta:
        model = Task
        exclude = ['id', 'task_state', 'created_datetime']
