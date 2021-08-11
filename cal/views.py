from cal.forms import EventForm
from datetime import datetime, timedelta
from django.shortcuts import get_object_or_404, render, get_list_or_404, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar

from .models import *
from .utils import Calendar


class CalendarView(generic.ListView):
    model = Event
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(pk=self.kwargs['pk'],withyear=True)
        context['group'] = Group.objects.get(id = self.kwargs['pk'])
        context['gid'] = self.kwargs['pk']
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        return context

    def index(request):
        title_list = Event.objects.order_by('-start_time')
        context = {'title_list': title_list}
        return render(request, 'cal/calendar.html', context)


def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return datetime(year, month, day=1)
    return datetime.today()


def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month


def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month


def event_new(request, pk):
    instance = Event()

    form = EventForm(request.POST or None, instance = instance)
    if request.POST and form.is_valid():
        cal = form.save(commit=False)
        cal.gid_id = pk
        cal.save()
        url = reverse('cal:calendar', kwargs={'pk': pk})
        return HttpResponseRedirect(url)
    context = {'form': form, 'pk':pk, 'group': Group.objects.get(id=pk)}
    return render(request, 'cal/event.html', context)

def event_edit(request, event_id=None):
    instance = get_object_or_404(Event, pk=event_id)
    flag = request.POST.get("flag")
    form = EventForm(request.POST or None, instance = instance)

    if request.POST and form.is_valid():
        event = form.save(commit=False)
        pk = event.gid.id
        if flag=="1" :
            event.save()
        else:
            event.delete()
        url = reverse('cal:calendar', kwargs={'pk': pk})
        return HttpResponseRedirect(url)

    else:
        form = EventForm(instance=instance)
        pk = instance.gid.id
        context = {'form': form, 'pk':pk, 'group': Group.objects.get(id=pk)}
    return render(request, 'cal/event.html', context)
