from django.contrib import admin

# Register your models here.
from django.contrib import admin

from .models import Feed, Entry, Group, GroupFeed

class EntryAdmin(admin.ModelAdmin):
    readonly_fields = ['entry_created']
class GroupAdmin(admin.ModelAdmin):
    list_display = ['description', 'id']

admin.site.register([Feed])
admin.site.register(Entry, EntryAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(GroupFeed)