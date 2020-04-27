from django.db import models
from product.models import Product
# Create your models here.

class Bug(models.Model):
    Product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField('bug 名称', max_length=64)  # Bug 名称
    BUG_STATUS = (('激活', '激活'), ('已解决', '已解决'), ('已关闭', '已关闭'))
    status = models.CharField(verbose_name='解决状态', choices=BUG_STATUS, default='激活 ', max_length=200)
    BUG_LEVEL = (('1', '1'), ('2', '2'), ('3', '3'))
    level = models.CharField(verbose_name='严重程度', choices=BUG_LEVEL, default='3', max_length=200)
    detail = models.CharField('详情', max_length=200)

    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)


    class Meta:
        verbose_name = 'bug 管理'
        verbose_name_plural = 'bug 管理'


    def __str__(self):
        return self.name
