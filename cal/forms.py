from django.db import models
from django.db.models import fields
from django.forms import ModelForm, DateInput, widgets
from cal.models import Event

class EventForm(ModelForm):
    class Meta:
        model = Event

        widgets ={
            'start_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
            'end_time': DateInput(attrs={'type': 'datetime-local'}, format='%Y-%m-%dT%H:%M'),
        }
        fields = ['title', 'description', 'start_time', 'end_time']

    def __init__(self, *args, **kwargs):
        super(EventForm, self).__init__(*args, **kwargs)
        self.fields['start_time'].input_formats = ('%Y-%m-%dT%H:%M',)
        self.fields['end_time'].input_formats = ('%Y-%m-%dT%H:%M',)