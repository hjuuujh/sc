
from board.models import Board

from board.models import Board
from django.contrib import admin
from .models import Board ,Post, Comment

# Register your models here.
admin.site.register(Board)
admin.site.register(Post)
admin.site.register(Comment)
