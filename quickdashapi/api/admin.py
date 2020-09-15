from .models import User, Entries, Source, SpeechTimeline, ScreenTimeline, Face
from django.contrib import admin


admin.site.register([User, Entries, Source, ScreenTimeline, SpeechTimeline, Face])
