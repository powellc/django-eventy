from django.contrib import admin
from eventy.models import *

class EventTimeAdmin(admin.ModelAdmin):
    list_display = ('event', 'start', 'end', 'place', )
    search_fields = ('event',)
    list_filter = ( 'place', 'event', )

admin.site.register(EventTime, EventTimeAdmin)
    
admin.site.register(Place)
admin.site.register(Calendar)
admin.site.register(Event)
