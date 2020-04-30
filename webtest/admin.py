from django.contrib import admin
from webtest.models import Page, Element, Case, CaseStep


# Register your models here.

class ElementAdmin(admin.TabularInline):
    list_display = ['page', 'elementname', 'targeting', 'value', 'create_at', 'update_at']
    # change_form_template = 'admin/extras/record_change_form.html'
    model = Element
    extra = 1


class PageAdmin(admin.ModelAdmin):
    list_display = ['product', 'pagename', 'create_at', 'update_at']
    inlines = [ElementAdmin]
    list_filter = ['product']
    list_display_links = ['pagename']


class CaseStepAdmin(admin.TabularInline):
    list_display = ['case', 'number', 'page', 'element', 'action']
    model = CaseStep
    extra = 1


class CaseAdmin(admin.ModelAdmin):
    list_display = ['id', 'casename', 'product', 'create_at', 'update_at']
    inlines = [CaseStepAdmin]
    list_display_links = ['casename']
    list_filter = ['product']
    change_form_template = 'admin/extras/case_change_form.html'


admin.site.register(Page, PageAdmin)
admin.site.register(Case, CaseAdmin)
