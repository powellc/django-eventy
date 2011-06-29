django-eventy
==================

Tired of rewriting urls for django schedule on each project and not
using most of it's features, eventy scratches an itch. What I have found
is that I am slowly adding back in most of schedule's features. Lesson
here: feature creep is inevitable to a certain degree.

That said, Eventy is still useful, and the urls are laid out in a more
sane way (in my opinion).

Basics
--------

Event - encapsulates info about overarching events
EventTime - a particular occurance of a given event
Calendar - a container full of events
Place - where an event takes place

Urls, as mentioned above, are setup to make intuitive sense (and to
forsake some aspects of DRY):

<code>List events in January 2011:
<urlhook>/2011/jan/08/

List events in calendar Specials
<urlhook>/specials/

List events in calendar Specials on Jan 8, 2011
<urlhook>/specials/2011/jan/08/

List event occurances for event "Super party tuesdays"
<urlhook>/super-party-tuesdays/

List event occurances for event "Super party tuesdays" in March 2010:
<urlhook>/super-party-tuesdays/2010/mar/</code>

That should give you a taste. Importantance has been placed on making
the URLs make intuitive sense to a user, even if they may repeat
themselves sometimes (i.e. not everything has only ONE uri). This setup
was based on actual user usage of a website with events and the 404s
that were generated as people tried to type or share urls that
django-schedule did not generate.



