from .models import User, Entries, Source, SpeechTimeline, ScreenTimeline, Face, AgeAll, AgeFemale, AgeMale
from django.contrib import admin


admin.site.register([User, Entries, Source, ScreenTimeline, SpeechTimeline, Face, AgeAll, AgeFemale, AgeMale])
