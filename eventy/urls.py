from django.conf.urls.defaults import *
from django.views.generic import ListView, DetailView
from eventy.models import Event, EventTime, Calendar, Place
from eventy.views import EventDetailView, EventDayView, EventMonthView, EventYearView, EventListView

urlpatterns = patterns('',
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$', view=EventDayView.as_view(),    name='ev-events-day'),
    url(r'^(?P<year>\d{4})/(?P<month>\w{3})/$',                  view=EventMonthView.as_view(),  name='ev-events-month'),
    url(r'^(?P<year>\d{4})/$',                                   view=EventYearView.as_view(),   name='ev-events-year'),

    url(r'^calendars/(?P<cal_slug>[-\w]+)/(?P<year>\d{4})/$',                  view=EventYearView.as_view(),   name='ev-calendar-year'),
    url(r'^calendars/(?P<cal_slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\w{3})/$', view=EventMonthView.as_view(),  name='ev-calendar-month'),
    url(r'^calendars/(?P<cal_slug>[-\w]+)/$',                                  view=EventListView.as_view(),   name='ev-calendar-detail'),
    url(r'^calendars/$',                                                       view=ListView.as_view(model=Calendar), name='ev-calendar-list'),

    url(r'^places/$', view=ListView.as_view(model=Place), name='place-list'),
    url(r'^places/(?P<slug>[-\w]+)/$', view=DetailView.as_view(model=Place), name='place-detail'),

    url(r'^(?P<slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\w{3})/(?P<day>\d{1,2})/$', view=EventDetailView.as_view(), name='ev-event-detail'),
    url(r'^(?P<slug>[-\w]+)/(?P<year>\d{4})/(?P<month>\w{3})/$',                  view=EventMonthView.as_view(),  name='ev-event-month'),
    url(r'^(?P<slug>[-\w]+)/(?P<year>\d{4})/$',                                   view=EventYearView.as_view(),   name='ev-event-year'),
    url(r'^(?P<slug>[-\w]+)/$',                                                   view=DetailView.as_view(model=Event), name='ev-events-info'),
    url(r'^$', view=EventListView.as_view(), name='event-list'),
)
