from django.contrib import admin

from result.models import ResultCount
# Register your models here.
class ResultCountAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'jobname', 'run_count', 'pass_count', 'fail_count', 'create_time']
    list_display_links = ['jobname']
    list_filter = ['product']

    verbose_name = '结果'

admin.site.register(ResultCount, ResultCountAdmin)