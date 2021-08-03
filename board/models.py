from django.db import models
from group.models import Group
from django.contrib.auth.models import User
from django.utils import timezone

class Board(models.Model):
    bname = models.CharField(max_length=100)
    gid = models.ForeignKey(Group, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.bname


class Post(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    bid = models.ForeignKey(Board, on_delete=models.CASCADE)
    gid = models.ForeignKey(Group, on_delete=models.CASCADE)
    create_date = models.DateTimeField(default=timezone.now)
    title = models.CharField(max_length=200)
    contents = models.TextField(max_length=1000)

    def __str__(self):
        return self.title


class Comment(models.Model):
    pid = models.ForeignKey(Post, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    contents = models.TextField(max_length=200)
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.contents
