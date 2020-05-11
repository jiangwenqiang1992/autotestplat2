import json
import time

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from selenium import webdriver

from product.models import Product
from webtest.models import CaseStep, Page, Element, Case
from webtest.runcase import RunCase

def runwebtest(request):
    runcase = RunCase()
    runcase.run()
    return HttpResponse('pk')


def get_page(request, obj_id):  # 根据product 获取page
    servers = Page.objects.filter(product=obj_id)
    result = []
    for i in servers:
        # 对应的id和ip组成一个字典
        result.append({'id': i.id, 'name': i.pagename})
    # 返回json数据
    return HttpResponse(json.dumps(result), content_type="application/json")


def get_element(request, obj_id):  # 根据page 获取element
    elements = Element.objects.filter(page=obj_id)
    result = []
    for i in elements:
        # 对应的id和ip组成一个字典
        result.append({'id': i.id, 'name': i.elementname})
    # 返回json数据
    return HttpResponse(json.dumps(result), content_type="application/json")
