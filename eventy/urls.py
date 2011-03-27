from django.conf.urls.defaults import *
from django.views.generic import ListView
from django.views.generic.date import 
from django.conf import settings
from eventy.models import Event, EventTime, Calendar, Place
from eventy.views import EventDetailView, EventDayView, EventMonthView, EventYearView, EventListView

urlpatterns = patterns('',
    (r'^(?P<slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$', EventDetailView.as_view(), name='event-detail'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/$',                  EventDayView.as_view(),    name='events-day'),
    (r'^(?P<year>\d{4})/(?P<month>\d{1,2})/$',                                   EventMonthView.as_view(),  name='events-month'),
    (r'^(?P<year>\d{4})/$',                                                      EventYearView.as_view(),   name='events-year'),
    
    (r'^(?P<slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\d{1,2})/$',                  EventMonthView.as_view(),  name='event-month'),
    (r'^(?P<slug>[-\w]+)/(?P<year>\d{4})/$',                                     EventYearView.as_view(),   name='event-year'),
    (r'^(?P<slug>[-\w]+)/$',                                                     DetailView.as_view(model=Event), name='event-info'),

    (r'^calendars/(?P<cal_slug>[-\w]+)/(?P<year>\d{1,2})/$',                     EventYearView.as_view(),   name='event-calendar-year'),
    (r'^calendars/(?P<cal_slug>[-\w]+)/(?P<year>\d{1,2})/(?P<month>\d{1,2})/$',  EventMonthView.as_view(),  name='event-calendar-month'),
    (r'^calendars/(?P<cal_slug>[-\w]+)/$',                                       EventListView.as_view(),   name='event-calendar-detail'),
    (r'^calendars/$',                                                            ListView.as_view(),        name='event-calendar-list'),
    
    (r'^places/$', ListView.as_view(model=Place)), 
    (r'^places/(?P<slug>[-\w]+)/$', DetailView.as_view(model=Place)), 
    
    (r'^$', EventListView.as_view()), 
)


