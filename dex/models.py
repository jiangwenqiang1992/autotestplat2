from django.db import models


# Create your models here.

class DEXTestResult(models.Model):
    CASE = ((1, "限价买单不成交"), (2, "限价买单成交"), (3, "市价买单成交"), (4, "限价卖单不成交"), (5, "限价卖单成交"), (6, "市价卖单成交"))
    case_type = models.SmallIntegerField('用例类型', choices=CASE)
    symbol = models.CharField('交易对', max_length=100)
    status = models.BooleanField('是否通过')
    remark = models.CharField('备注', max_length=1000, null=True, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)

    class Meta:
        verbose_name = 'DEX测试结果'

    def __str__(self):
        return str(self.case_type)
