from dateutil.relativedelta import relativedelta
from datetime import datetime
import logging

from django.template.context import RequestContext
from django.views.generic import ListView, DetailView
from django.views.generic.dates import DateDetailView, YearArchiveView, MonthArchiveView, DayArchiveView
from django.shortcuts import render_to_response, get_object_or_404

from eventy.models import EventTime, Calendar, Event
from eventy.utils import EventCalendar 

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
        context['month'] = EventCalendar(self.get_queryset()).formatmonth(datetime.now().year, datetime.now().month)
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
    allow_empty = True

    def get_queryset(self):
        try:
            if self.kwargs['cal_slug']:
                return EventTime.upcoming_objects.filter(event__calendar__slug=self.kwargs['cal_slug'])
        except:
            pass

        try:
            if self.kwargs['slug']:
                return EventTime.upcoming_objects.filter(event__slug=self.kwargs['slug'])
        except:
            logging.debug('Returning all upcoming events...')
            return EventTime.upcoming_objects.all()

    def get_context_data(self, **kwargs):
        context = super(EventYearView, self).get_context_data(**kwargs)
        try:
            context['next_date'] = context['date_list'][0] + relativedelta(years=1)
            context['prev_date'] = context['date_list'][0] - relativedelta(years=1)
        except:
            pass
        return context

class EventMonthView(MonthArchiveView):
    context_object_name = "event_list"
    allow_future = True
    date_field = 'start'
    allow_empty = True

    def get_queryset(self):
        try:
            if self.kwargs['cal_slug']:
                return EventTime.upcoming_objects.filter(event__calendar__slug=self.kwargs['cal_slug'])
        except:
            pass

        try:
            if self.kwargs['slug']:
                return EventTime.upcoming_objects.filter(event__slug=self.kwargs['slug'])
        except:
            return EventTime.upcoming_objects.all()

    def get_context_data(self, **kwargs):
        context = super(EventMonthView, self).get_context_data(**kwargs)
        try:
            context['next_date'] = next_date = context['date_list'][0] + relativedelta(months=1)
            context['prev_date'] = prev_date = context['date_list'][0] - relativedelta(months=1)
            context['next_month_str'] = next_date.strftime('%b').lower()
            context['prev_month_str'] = prev_date.strftime('%b').lower()
        except:
            pass
        logging.debug('Month is: %s' % context)
        return context
    
class EventDayView(DayArchiveView):
    context_object_name = "event_list"
    queryset=EventTime.upcoming_objects.all()
    allow_future = True
    date_field = 'start'
    allow_empty = True
