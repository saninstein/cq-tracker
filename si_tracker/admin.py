from django.contrib import admin
from si_tracker.models import *

class IssuesAdmin(admin.ModelAdmin):
    exclude = ()

admin.site.register(Issue)
admin.site.register(Task)
