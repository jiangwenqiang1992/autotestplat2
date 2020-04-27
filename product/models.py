from django.db import models


# app名+类名，即表名
class Product(models.Model):
    # CharField 表示字符串类型（第一个参数是别名，max_length是最长字节&必填,unique表示唯一）
    name = models.CharField('产品名称', max_length=200, unique=True)  # 产品名称

    # TextField 表示长文本类型
    # （null=True表示可以为空，blank=True表示表单提交时可以为空）默认是False
    devconfig = models.TextField('开发环境配置', null=True, blank=True)
    testconfig = models.TextField('测试环境配置', null=True, blank=True)
    prodconfig = models.TextField('生产环境配置', null=True, blank=True)

    # DateTimeFiel 表示时间类型，（auto_now_add=True 表示自动创建）
    create_time = models.DateTimeField('创建时间', auto_now_add=True)  # 创建时间，自动获取# 当前时间

    # （auto_now=True） 表示自动更新
    update_time = models.DateTimeField('更新时间', auto_now=True)  # 创建时间，自动获取# 当前时间

    # 设置表的属性
    class Meta:

        # 别名
        verbose_name = '项目和配置'
        verbose_name_plural = '项目和配置'


    def __str__(self):
        return self.name