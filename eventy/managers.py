from datetime import datetime
from django.db.models import Manager
from django.db.models import Q

class UpcomingManager(Manager):
    """Returns upcoming events."""

    def get_query_set(self):
        return super(UpcomingManager, self).get_query_set().filter(start__gte=datetime.now())
