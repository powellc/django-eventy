from datetime import datetime

from django.template.context import RequestContext
from django.views.generic import ListView, DetailView
from django.views.generic.dates import DateDetailView, YearArchiveView, MonthArchiveView, DayArchiveView
from django.shortcuts import render_to_response, get_object_or_404

from eventy.models import EventTime, Calendar

class EventListView(ListView):
    ''' EventListView
    Extend ListView with EventTime objects and load a calendar if the cal_slug is present.
    '''
    context_object_name = "event_list"
    date_field = 'start'

    def get_queryset(self):
        try:
            cal_slug = self.kwargs['cal_slug']
            self.calendar = get_object_or_404(Calendar, slug=cal_slug)
        except:
            self.calendar = None
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
    date_field = 'start'

class EventYearView(YearArchiveView):
    context_object_name = "event_list"
    allow_future = True
    date_field = 'start'

    def get_queryset(self):
        try:
            if self.kwargs['cal_slug']:
                return EventTime.upcoming_objects.filter(event__calendar__slug=self.kwargs['cal_slug'])
        except:
            pass

        if self.kwargs['slug']:
            return EventTime.upcoming_objects.filter(event__slug=self.kwargs['slug'])
        else:
            return EventTime.upcoming_objects.all()

class EventMonthView(MonthArchiveView):
    context_object_name = "event_list"
    allow_future = True
    date_field = 'start'

    def get_queryset(self):
        try:
            if self.kwargs['cal_slug']:
                return EventTime.upcoming_objects.filter(event__calendar__slug=self.kwargs['cal_slug'])
        except:
            pass
        if self.kwargs['slug']:
            return EventTime.upcoming_objects.filter(event__slug=self.kwargs['slug'])
        else:
            return EventTime.upcoming_objects.all()
    
class EventDayView(DayArchiveView):
    context_object_name = "event_list"
    queryset=EventTime.upcoming_objects.all()
    allow_future = True
    date_field = 'start'
