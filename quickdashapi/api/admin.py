from .models import User, Entries, Source
from django.contrib import admin


admin.site.register([User, Entries, Source])
