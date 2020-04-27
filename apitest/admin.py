from django.contrib import admin

# Register your models here.
from apitest.models import Apicase
from apitest.models import Step, Api, Process

class ApisAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'name', 'path', 'method', 'create_time']
    # 在界面上增加筛选
    list_filter = ['product']


admin.site.register(Apicase, ApisAdmin)




# TabularInline 表示该类属于表格内联（到界面时就知道什么意思）
class StepAdmin(admin.TabularInline):
    list_display = ['id', 'process', 'number', 'api']
    model = Step  # 指定关联模型
    extra = 1  #


class ApiAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'name', 'path', 'create_time']
    list_display_links = ['name']  # 指定列表中该字段可以点击（打开编辑页面）
    list_filter = ['product']  # 添加过滤器


class ProcessAdmin(admin.ModelAdmin):
    list_display = ['id', 'product', 'name', 'create_time', 'update_time']
    list_display_links = ['name']
    inlines = [StepAdmin]  # 添加/编辑api时，可以同时添加/编辑多个step
    list_filter = ['product']


admin.site.register(Api, ApiAdmin)
admin.site.register(Process, ProcessAdmin)
