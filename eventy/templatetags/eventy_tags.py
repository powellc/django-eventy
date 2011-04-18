from datetime import datetime, timedelta
import logging
from django.db import models
from django.conf import settings
from django import template
from django.core.urlresolvers import reverse
from django.utils.dateformat import format
from eventy.models import Calendar, EventTime
from eventy.utils import EventCalendar

register = template.Library()

def do_get_next_events(parser, token):
    ''' Gets a number of upcoming events for a given calendar slug and loads a template variable.

        Example usage:

        {% get_next_events 5 from vacation as events %} 
        {% get_next_events 5 from all as events %} 
        {% get_next_events 5 from all but services as events %} 
        {% get_next_events 5 from all but services,office as events %} 

    '''

    args = token.split_contents()
    argc = len(args)

    try:
        assert argc in (6, 8)
    except AssertionError:
        raise template.TemplateSyntaxError('Invalid get_committee_groups syntax.')
    # determine what parameters to use
    limit = cal_slug = excluded_cals = varname = None
    if argc == 6: t, limit, f, cal_slug, a, varname = args
    elif argc == 8: t, limit, f, cal_slug, b, excluded_cals, a, varname = args
    return GetNextEventsNode(limit=limit, calendar_slug=cal_slug, excluded_cals=excluded_cals, varname=varname)

class GetNextEventsNode(template.Node):
    def __init__(self, limit, calendar_slug, excluded_cals, varname):
        self.limit, self.varname, self.calendar_slug, = int(limit), varname, calendar_slug
        try:
            self.excluded_cals = excluded_cals.split(',')
        except:
            self.excluded_cals = []

    def render(self, context):
        if self.calendar_slug == 'all':
            events = EventTime.upcoming_objects.all().order_by('start')
        else:
            events = EventTime.upcoming_objects.filter(event__calendar__slug=self.calendar_slug).order_by('start')

        if self.excluded_cals:
            for cal_slug in self.excluded_cals:
                events = events.exclude(event__calendar__slug=cal_slug)

        logging.debug('Fetching %s events from calendar %s excluding %s.' % (self.limit, self.calendar_slug, self.excluded_cals))
        if self.limit == 1:
            try:
                context[self.varname] = events[0]
            except:
                context[self.varname] = None
        else:
            try:
                context[self.varname] = events[:self.limit]
            except:
                context[self.varname] = None
        return ''

register.tag("get_next_events", do_get_next_events)

@register.inclusion_tag('eventy/_month_table.html')
def show_month(events, date, size="large"):
    if date == '':
        month_table = EventCalendar(events, size).formatmonth(datetime.now().year, datetime.now().month)
    else:
        month_table = EventCalendar(events, size).formatmonth(date.year, date.month)
    return {'month_table':month_table, 'size':size }

@register.inclusion_tag('eventy/_year_table.html')
def show_year(events, date, size="small"):
    year_table = EventCalendar(events, size).formatyear(int(date))
    return {'year_table':year_table }
