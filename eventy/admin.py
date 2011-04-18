from django.contrib import admin
from eventy.models import *

class EventTimeAdmin(admin.ModelAdmin):
    list_display = ('event', 'start', 'end', 'place', )
    search_fields = ('event',)
    list_filter = ( 'place', 'event', )

admin.site.register(EventTime, EventTimeAdmin)

class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'calendar', 'submitted_by',)
    search_fields = ('title','calendar',)
    list_filter = ('calendar', )

admin.site.register(Event, EventAdmin)
    
admin.site.register(Place)
admin.site.register(Calendar)
