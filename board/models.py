import uuid

from django.db import models


class Board(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=64)
    description = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class TaskState(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField()
    index = models.PositiveIntegerField()
    created_datetime = models.DateTimeField(auto_now_add=True)
    something = models.OneToOneField

    def __str__(self):
        return self.name

class Task(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    task_state = models.ForeignKey(TaskState, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    description = models.TextField()
    created_datetime = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

"""

"""