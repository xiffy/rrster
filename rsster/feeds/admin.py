from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Feed, Entry

class EntryAdmin(admin.ModelAdmin):
    readonly_fields = ['entry_created']

admin.site.register([Feed])
admin.site.register(Entry, EntryAdmin)