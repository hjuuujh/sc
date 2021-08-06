from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User




class Group(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)  # 그룹이름
    info = models.CharField(max_length=200)  # 그룹 소개
    goal = models.CharField(max_length=300)  # 그룹 목표
    members = models.IntegerField(default=0)  # 그룹 인원수
    max_members = models.IntegerField(default=0)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['-id']


class Join(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)  # user 아이디
    gid = models.ForeignKey(Group, on_delete=models.CASCADE)  # 그룹
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (("uid","gid"),)


class JoinRequest(models.Model):
    uid = models.ForeignKey(User, on_delete=models.CASCADE)  # user 아이디
    gid = models.ForeignKey(Group, on_delete=models.CASCADE)  # 그룹
    motivation = models.CharField(max_length=100)
    date = models.DateTimeField(default=timezone.now)

    class Meta:
        unique_together = (("uid","gid"),)