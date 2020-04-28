from django.db import models

# Create your models here.
from product.models import Product


class Apicase(models.Model):
    # 外键，一对多，一个product，对多个apicase
    # related_name 可提供外键表对象查询子表数据 product.apicase
    # on_delete=models.CASCADE 外键删除时，同时删除子表关联数据
    product = models.ForeignKey(Product, related_name="apicase",
                                on_delete=models.CASCADE)  # 关联产品 ID
    name = models.CharField('用例名称', max_length=100)
    path = models.CharField('路径', max_length=200, null=True, blank=True)
    headers = models.TextField('请求头', null=True, blank=True)
    REQUEST_METHOD = (('get', 'get'), ('post', 'post'), ('put', 'put'),
                      ('delete', 'delete'), ('patch', 'patch'))
    # choices 表示枚举类型，值是tuple类型
    # default 表示默认值
    method = models.CharField('请求方法', choices=REQUEST_METHOD,
                              default='post', max_length=200)
    param = models.TextField('请求参数和值,parametrize表示参数化', null=True, blank=True)
    parametrize = models.TextField('参数化', null=True, blank=True)
    expect = models.CharField('预期结果', max_length=200)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '单一接口用例'
        verbose_name_plural = '单一接口用例'

    def __str__(self):
        return self.name

class Process(models.Model):
    product = models.ForeignKey(Product, verbose_name='所属产品', related_name='process', on_delete=models.CASCADE)
    name = models.CharField('流程接口名称', max_length=64)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    update_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '流程场景用例'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name

class Api(models.Model):
    product = models.ForeignKey(Product, related_name='api', on_delete=models.CASCADE)
    name = models.CharField('名称', max_length=100)
    path = models.CharField('path', max_length=200, null=True, blank=True)
    headers = models.TextField('请求头', max_length=800, null=True,blank=True)
    param = models.TextField('请求参数值', max_length=800, null=True, blank=True)
    REQUEST_METHOD = (('get', 'get'), ('post', 'post'), ('put', 'put'),
                      ('delete', 'delete'), ('patch', 'patch'))
    method = models.CharField(verbose_name='请求方法', choices=REQUEST_METHOD,
                              default='get', max_length=200, null=True)
    expect = models.TextField('预期结果', max_length=200)
    extract = models.TextField('提取数据', max_length=200, null=True, blank=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    updata_time = models.DateTimeField('更新时间', auto_now=True)

    class Meta:
        verbose_name = '流程场景接口'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Step(models.Model):
    process = models.ForeignKey(Process, related_name="step", verbose_name="流程用例", on_delete=models.CASCADE)
    number = models.SmallIntegerField('序号')
    api = models.ForeignKey(Api, verbose_name="接口", on_delete=models.CASCADE)
    desc = models.TextField('描述')

    class Meta:
        verbose_name = '关联用例和接口'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.number)
