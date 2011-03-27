import datetime

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel
from eventy.managers import UpcomingManager

class Place(TitleSlugDescriptionModel, TimeStampedModel):
    address=models.CharField(_('Address'), max_length=150)
    city=models.CharField(_('City'), max_length=150)
    state=USStateField(_('State'))
    zipcode=models.IntegerField(_('Zipcode'), max_length=9)

    class Meta:
        verbose_name = _('place')
        verbose_name_plural = _('places')

    def __unicode__(self):
        return self.title

class Calendar(TitleSlugDescription, TimeStampedModel):
    """Calendar model."""

    class Meta:
        verbose_name = _('calendar')
        verbose_name_plural=_('calendars')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('calendar_detail', None, { 'slug': self.slug, })

class Event(TitleSlugDescription, TimeStampedModel):
    """Event model"""
    calendar=models.ForeignKey(Calendar, blank=True, null=True)
    place = models.ForeignKey(Place, blank=True, null=True)
    place_string = models.CharField(_('One-off place'), max_length=200, blank=True)
    submitted_by = models.ForeignKey(User, blank=True, null=True)

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return ('event_info', None, { 'slug': self.event.slug, })

class EventTime(models.Model):
    """EventTime model
    
    This model does most of the heavy lifting as to whether """
    event = models.ForeignKey(Event, related_name='event_times')
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    is_all_day = models.BooleanField(default=False)

    objects = models.Manager()
    upcoming_objects = UpcomingManager()

    class Meta:
        verbose_name = _('event time')
        verbose_name_plural = _('event times')

    @property
    def is_past(self):
        NOW = datetime.date.now()
        if self.start < NOW:
            return True
        return False

    def __unicode__(self):
        return u'%s' % self.event.title

    @permalink
    def get_absolute_url(self):
        return ('event-detail', None, {
            'year': self.start.year,
            'month': self.start.strftime('%b').lower(),
            'day': self.start.day,
            'slug': self.event.slug,
        })
