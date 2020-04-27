from django.db import models

# Create your models here.
from product.models import Product


class ResultCount(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    jobname = models.CharField('任务名称', max_length=100)
    run_count = models.SmallIntegerField('运行用例数')
    pass_count = models.SmallIntegerField('通过用例数')
    fail_count = models.SmallIntegerField('失败用例数')
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '运行结果统计'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.jobname
