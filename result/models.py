from django.db import models

# Create your models here.
from product.models import Product


class ResultCount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    jobname = models.CharFeild('任务名称', max_lenth=100)
    run_count = models.SmartIntFeild('运行用例数')
    pass_count = models.SmartIntFeild('通过用例数')
    fail_count = models.SmartIntFeild('失败用例数')
    create_time = models.DateTimeFeild('创建时间', auto_time_add=True)
    update_time = models.DateTimeFeild('更新时间', auto_time=True)

    class Meta():
        verbose_name = '运行结果统计'
        verbose_name_prul = verbose_name

    def __str__():
        return self.jobname
