from django import forms
from board.models import *


class PostForm(forms.ModelForm):
    class Meta:
        model = Post  # 사용할 모델
        fields = ['title', 'contents','file']  # 게시글 제목, 내용, 이미지파일
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'contents': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
        }
        labels = {
            'title': '제목',
            'contents': '내용',
            'file' : 'Image File'
        }
    
    def __init__(self, *args, **kwargs):
        super(PostForm, self).__init__(*args, **kwargs)
        self.fields['file'].required = False



class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['contents']
        labels = {
            'contents': '댓글 내용',
        }
        widgets = {
            'contents': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'contents': '내용',
        }
        
class BoardForm(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['bname']
        labels = {
            'bname': forms.TextInput(attrs={'class': 'form-control'}),
        }
        widgets = {
            'bname': forms.TextInput(attrs={'class': 'form-control'}),
        }
        labels = {
            'bname': '게시판 이름',
        }
