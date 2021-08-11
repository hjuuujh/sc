from django.db import models
from group.models import Group
from django.contrib.auth.models import User
from django.utils import timezone
import os
from django.conf import settings


class Board(models.Model):
    bname = models.CharField(max_length=100)
    gid = models.ForeignKey(Group,on_delete=models.CASCADE)
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
    post_hit = models.PositiveIntegerField(default = 0)
    file = models.ImageField(null=True , upload_to="", blank=True)   # 이미지파일 
    

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-create_date']
    
    @property
    def update_counter(self):
        self.post_hit += 1 
        self.save()
    
    # 게시글 삭제 시 media 디렉토리에 있는 사진도 같이 삭제
    def delete(self, *args, **kargs):
        if self.file:
            os.remove(os.path.join(settings.MEDIA_ROOT, self.file.path))
        super(Post, self).delete(*args, **kargs)


class Comment(models.Model):
    pid = models.ForeignKey(Post, on_delete=models.CASCADE)
    uid = models.ForeignKey(User, on_delete=models.CASCADE)
    contents = models.TextField(max_length=200)
    create_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.contents
