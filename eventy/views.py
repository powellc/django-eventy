from datetime import datetime

from django.template.context import RequestContext
from django.views.generic import ListView, DetailView
from django.views.generic.dates import DateDetailView, DateArchiveView, YearArchiveView, MonthArchiveView, DayArchiveView
from django.shortcuts import render_to_response, get_object_or_404

from eventy.models import EventTime, Calendar

class EventListView(ListView)
    ''' EventListView
    Extend ListView with EventTime objects and load a calendar if the cal_slug is present.
    '''
    context_object_name = "event_list"

    def get_queryset(self):
        if self.kwargs['cal_slug'}:
            self.calendar = get_object_or_404(Calendar, slug=self.kwargs['cal_slug']) 
        return EventTime.upcoming_objects.all()

    def get_context_data(self, **kwargs):
        context = super(EventListView, self).get_context_data(**kwargs)
        if self.calendar:
            context['calendar'] = self.calendar
        return context

class EventDetailView(DateDetailView):
    context_object_name = "event"
    queryset=EventTime.upcoming_objects.all()
    allow_future = True

class EventYearView(YearArchiveView):
    context_object_name = "event_list"
    allow_future = True

    def get_queryset(self):
        if self.kwargs['cal_slug'}:
            return EventTime.upcoming_objects.filter(event__calendar__slug=self.kwargs['cal_slug'])
        elif self.kwarg['slug']:
            return EventTime.upcoming_objects.filter(event__slug=self.kwargs['slug'])
        else:
            return EventTime.upcoming_objects.all()

class EventMonthView(MonthArchiveView):
    context_object_name = "event_list"
    allow_future = True

    def get_queryset(self):
        if self.kwargs['cal_slug'}:
            return EventTime.upcoming_objects.filter(event__calendar__slug=self.kwargs['cal_slug'])
        elif self.kwarg['slug']:
            return EventTime.upcoming_objects.filter(event__slug=self.kwargs['slug'])
        else:
            return EventTime.upcoming_objects.all()
    
class EventDayView(DayArchiveView):
    context_object_name = "event_list"
    queryset=EventTime.upcoming_objects.all()
    allow_future = True
