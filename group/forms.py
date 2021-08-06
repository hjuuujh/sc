from django import forms
from group.models import Group, Join

# 그룹 생성 폼
class GroupForm(forms.ModelForm):

    class Meta:
        model = Group
        fields = ['name', 'info', 'goal', 'max_members']

        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'info': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'goal': forms.TextInput(attrs={'class': 'form-control', 'rows': 10}),
            'max_members': forms.NumberInput(attrs={'class': 'form-control', 'rows': 10})


        }
        labels = {
                'name' : '그룹 이름',
                 'info' : '그룹 정보',
                 'goal' : '그룹 목표',
                 'max_members': '최대 인원',
                }



