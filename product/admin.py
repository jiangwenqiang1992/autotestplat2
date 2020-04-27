from django.contrib import admin

from product.models import Product
from apitest.models import Step, Api, Process


# 创建product管理类，继承admin.ModelAdmin
class ProductAdmin(admin.ModelAdmin):
    # list_display 是限制后台管理-product列表显示的字段（字段名必须在product类存在）
    list_display = ['id', 'name', 'create_time', 'update_time']


# 把产品模块注册到 Django admin 后台才能显示
# （第一个参数是数据对象类，第二个是对应管理类）
admin.site.register(Product, ProductAdmin)


