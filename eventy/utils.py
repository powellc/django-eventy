import calendar
import logging
from datetime import date
from itertools import groupby

from django.utils.html import conditional_escape as esc

class EventCalendar(calendar.HTMLCalendar):
    def __init__(self, events, size='large'):
        super(EventCalendar, self).__init__()
        self.events = self.group_by_day(events)
        self.size = size
    
    def formatday(self, day, weekday):
        if day != 0:
            cssclass = self.cssclasses[weekday]
            if date.today() == date(self.year, self.month, day):
                cssclass += ' today'
            if day in self.events:
                cssclass += ' filled'
                if self.size == 'large':
                    body = ['<ul>']
                    for event in self.events[day]:
                        body.append('<li>')
                        body.append('<a href="%s">' % event.get_absolute_url())
                        body.append(esc(event.event.title))
                        body.append('</a></li>')
                        body.append('</ul>')
                    return self.day_cell(cssclass, '%d %s' % (day, ''.join(body)))
                else:
                    for event in self.events[day]:
                        body = ['<a href="%s"><div class="%s">%d</div></a>' % (event.get_absolute_url(), event.event.calendar.slug, day)]
                    return self.day_cell(cssclass, '%s' % ''.join(body))
            return self.day_cell(cssclass, '%d %s' % (day, ''.join('<div class="noevents"></div>')))
        return self.day_cell('noday', '&nbsp;')

    def formatmonth(self, year, month, **kwargs):
        self.year, self.month = year, month
        return super(EventCalendar, self).formatmonth(year, month, 100)

    def formatyear(self, year):
        self.year = year
        return super(EventCalendar, self).formatyear(year)

    def group_by_day(self, events):
        field = lambda event: event.start.day
        return dict([(day, list(items)) for day, items in groupby(events, field)])

    def day_cell(self, cssclass, body):
        return '<td class="%s">%s</td>' % (cssclass, body)
