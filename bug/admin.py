from django.contrib import admin

# Register your models here.
from bug.models import Bug


class BugAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'name', 'status', 'level', 'create_time']
    list_display_links = ['name']
    list_filter = ['product']


admin.site.register(Bug, BugAdmin)
