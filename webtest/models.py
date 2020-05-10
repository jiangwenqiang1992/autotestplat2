from django.db import models

# Create your models here.
from django.db import models


# Create your models here.
class Page(models.Model):
    product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    pagename = models.CharField(max_length=200, unique=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "页面"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.pagename


class Element(models.Model):
    # product = models.ForeignKey('product.Product', on_delete=models.CASCADE)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    elementname = models.CharField(max_length=200)
    target_choice = (
    ('1', 'id'), ("2", 'name'), ("3", 'class'), ("4", 'link_text'), ("5", 'tag_name'), ("6", 'css_selector'),
    ("7", 'xpath'), ("0", 'coordinate'))
    targeting = models.CharField(max_length=10, choices=target_choice, default=1)
    value = models.CharField(max_length=200)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "元素"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.elementname


class Case(models.Model):
    product = models.ForeignKey('product.Product', related_name='case', on_delete=models.CASCADE)
    casename = models.CharField(max_length=200, unique=True)
    pre_case = models.CharField(max_length=200, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "用例"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.casename


class CaseStep(models.Model):
    case = models.ForeignKey(Case, related_name='step', on_delete=models.CASCADE)
    number = models.SmallIntegerField('序号')
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    element = models.ForeignKey(Element, on_delete=models.CASCADE, null=True)
    action_choice = (("1", 'click'), ("2", 'sendstr'), ("3", 'moveto'))
    action = models.CharField(max_length=200, choices=action_choice)
    value = models.CharField(max_length=200, null=True, blank=True)
    assertdata = models.CharField(max_length=200, null=True, blank=True)
    extract = models.CharField(max_length=200, null=True, blank=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "用例步骤"
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.number)
