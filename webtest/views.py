import time

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from selenium import webdriver

from product.models import Product
from webtest.models import CaseStep
from webtest.util.mydriver import MyWebDriver


def runwebtest(request):
    #cases = Product.objects.get(productname='官网').case.all()

    #options = webdriver.ChromeOptions()
    #options.add_argument(r'--user-data-dir=C:\Users\Administrator\AppData\Local\Google\Chrome\User Data')

    #driver = webdriver.Chrome(chrome_options=options)  # 创建Chrome对象.
    driver = webdriver.Firefox()
    driver.maximize_window()

    # driver.find_element_by_id('')
    driver.get('https://www.waykichain.com')  # get方式访问百度.
    #
    # print(cases)
    # for case in cases:
    #     steps = CaseStep.objects.filter(case=case).all()
    #     for step in steps:
    #         time.sleep(1.5)
    #         element = step.element
    #         target = element.targeting
    #         target_value = element.value
    #         action = step.action
    #         action_value = step.value
    #         print(element.elementname, target, target_value, action, action_value)
    #         MyWebDriver(driver).TargetEnum(target, target_value).actionEnum(action, action_value)
    time.sleep(10)
    driver.quit()
    return HttpResponse('pk')
