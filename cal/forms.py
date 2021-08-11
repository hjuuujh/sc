from django.db import models
from django.db.models import fields
from django.forms import ModelForm, DateInput, widgets
from cal.models import Event
from django import forms

class EventForm(ModelForm):
    class Meta:
        model = Event
        fields = ['title', 'description', 'start_time', 'end_time']

        widgets ={
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 10}),
            'start_time': DateInput(attrs={'type': 'datetime-local','class': 'form-control'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local','class': 'form-control'}, format='%Y-%m-%dT%H:%M'),
        }

        labels = {
            'title': '일정 제목',
            'description': '일정 내용',
            'start_time': '시작 날짜',
            'end_time': '마지막 날짜',
        }

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)