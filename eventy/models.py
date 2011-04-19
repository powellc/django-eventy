from datetime import datetime

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic
from django.utils.translation import ugettext_lazy as _
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.localflavor.us.models import USStateField

from onec_utils.models import USAddressPhoneMixin
from django_extensions.db.models import TimeStampedModel, TitleSlugDescriptionModel

from eventy.managers import UpcomingManager

class Place(TitleSlugDescriptionModel, TimeStampedModel, USAddressPhoneMixin):

    class Meta:
        verbose_name = _('place')
        verbose_name_plural = _('places')

    def __unicode__(self):
        return self.title

class Calendar(TitleSlugDescriptionModel, TimeStampedModel):
    """Calendar model."""

    class Meta:
        verbose_name = _('calendar')
        verbose_name_plural=_('calendars')

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('event-calendar-detail', None, { 'cal_slug': self.slug, })

class Event(TitleSlugDescriptionModel, TimeStampedModel):
    """Event model"""
    calendar=models.ForeignKey(Calendar, blank=True, null=True)
    submitted_by = models.ForeignKey(User, blank=True, null=True)

    class Meta:
        verbose_name = _('event')
        verbose_name_plural = _('events')

    def __init__(self, *args, **kwargs):
        super (Event, self).__init__(*args, **kwargs)
        self._upcoming = None
        self._past = None

    @property
    def upcoming_event_times(self):
        if not self._upcoming:
            try:
                times = self.event_times.all().filter(start__gte=datetime.now().date)
            except(Event.DoesNotExist, IndexError):
                times = None
            self._upcoming = times
        return self._upcoming


    @property
    def past_event_times(self):
        if not self._past:
            try:
                times = self.event_times.all().filter(start__lte=datetime.now().date)
            except(Event.DoesNotExist, IndexError):
                times = None
            self._past= times
        return self._past

    def __unicode__(self):
        return self.title

    @models.permalink
    def get_absolute_url(self):
        return ('event-info', None, { 'slug': self.event.slug, })


class EventTime(models.Model):
    """EventTime model
    
    This model does most of the heavy lifting as to whether """
    event = models.ForeignKey(Event, related_name='event_times')
    start = models.DateTimeField()
    end = models.DateTimeField(blank=True, null=True)
    place = models.ForeignKey(Place, blank=True, null=True)
    place_string = models.CharField(_('One-off place'), max_length=200, blank=True)
    is_all_day = models.BooleanField(default=False)
    notes = models.TextField(_('Notes'), blank=True, null=True)
    slug = models.SlugField(_('Event slug'), blank=True, editable=False)

    objects = models.Manager()
    upcoming_objects = UpcomingManager()

    class Meta:
        verbose_name = _('event time')
        verbose_name_plural = _('event times')
        get_latest_by = 'start'

    def __init__(self, *args, **kwargs):
        super (EventTime, self).__init__(*args, **kwargs)
        self._next = None
        self._previous = None

    @property
    def is_past(self):
        NOW = datetime.now().date
        if self.start < NOW:
            return True
        return False

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.event.slug

        if self.place and not self.place_string:
            self.place_string = self.place.__unicode__()
        super(EventTime, self).save(*args, **kwargs)

    def __unicode__(self):
        return u'%s' % self.event.title

    @models.permalink
    def get_absolute_url(self):
        return ('ev-event-detail', None, {
            'year': self.start.year,
            'month': self.start.strftime('%b').lower(),
            'day': self.start.day,
            'slug': self.event.slug,
        })

    def get_next_event_time(self):
        """Determines the next event time"""

        if not self._next:
            try:
                qs = EventTime.objects.filter(event=self.event).exclude(id__exact=self.id)
                event_time= qs.filter(start__gte=self.start).order_by('start')[0]
            except (EventTime.DoesNotExist, IndexError):
                event_time = None
            self._next = event_time

        return self._next

    def get_previous_event_time(self):
        """Determines the previous event time"""

        if not self._previous:
            try:
                qs = EventTime.objects.all().exclude(id__exact=self.id)
                event_time= qs.filter(start__lte=self.start).order_by('-start')[0]
            except (EventTime.DoesNotExist, IndexError):
                event_time = None
            self._previous = event_time

        return self._previous

class RelatedEvent(models.Model):
    eventtime = models.ForeignKey(EventTime)
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey('content_type', 'object_id')

    def __unicode__(self):
        return self.eventtime.event.__unicode__()
