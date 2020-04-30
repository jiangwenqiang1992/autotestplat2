import json
import re

from bug.models import Bug
from product.models import Product
import requests
from result.models import ResultCount


class RunApiCase:
    count_pass = 0
    count_fail = 0
    count_run = 0
    product = None
    # 处理请求头数据
    def initHeader(self, headers):
        try:
            # 这里写初始化内容
            if headers == '' or headers is None:
                headers = {'content-type': 'application/json',
                           'Accept': 'application/json'}
        except Exception as e:
            raise Exception("headers init erro: {}".format(e))
        return headers

    # 处理请求内容数据
    def initParam(self, param):
        try:
            # 这里写初始化内容
            pass
        except Exception as e:
            raise Exception("param init erro: {}".format(e))
        return param

    # 发出请求
    def requestEnum(self, method, url, headers, param):
        if method == 'get':
            return requests.get(url, json=param, headers=headers)
        elif method == 'post':
            return requests.post(url, json=param, headers=headers)

    # 响应断言
    def responseAssert(self, expected, response):
        data = str(expected).split(',')
        for d in data:
            if d not in str(response):
                raise Exception('未找到断言参数:{}'.format(d))

    # 提取参数
    def extract(self, jsondata, extract_re, extract_param):
        if len(extract_re) == 0: return extract_param
        extract_re = str(extract_re).split('\n')
        for ex in extract_re:
            k, v = ex.split('=')
            data = re.search(v, json.dumps(jsondata))[0]
            if data:
                raise IndexError("未找到匹配对象{}".format(v))
            extract_param[k] = data
        return extract_param
        # print('extract_param',extract_param)


    # 提交BUG
    def submitBug(self, product, title, detail):
        bug = Bug(product=product, name=title, detail=detail)
        bug.save()

    # 提交结果统计
    def submitResult(self, product):
        result = ResultCount(product=product,jobname='baas服务生产测试',
                             run_count=self.count_run, pass_count=self.count_pass, fail_count=self.count_fail)
        result.save()


class BaasApi(RunApiCase):
    def __init__(self):
        self.product = Product.objects.get(name='baas服务')

    def runAll(self):
        apicase_list = self.product.apicase.all()
        self.count_run = len(apicase_list)

        for apicase in apicase_list:
            self.runCase(apicase)

        # 6、提交结果
        self.submitResult(self.product)
        return "pass:{}, fail:{}".format(self.count_pass, self.count_fail)

    def runCase(self, apicase):
        try:
            headers = self.initHeader(apicase.headers)
            param = self.initParam(apicase.param)

            # 如果有参数化
            if apicase.parametrize != '':
                # 把参数化数据格式化
                parametrize = str(apicase.parametrize).replace("'", '').replace('"', '') \
                    .replace(' ', '').replace('\n', '').replace('\r', '').split(',')
                for value in parametrize:
                    # 替换参数
                    param = str(param).replace('parametrize', value)
                    param = eval(param)
                    # 4、发出请求
                    method = apicase.method
                    url = "https://baas.wiccdev.org/v2/api" + apicase.path
                    response = self.requestEnum(method, url, headers, param).text
                    print(apicase.name, ' ', response)
                    # 5、响应断言
                    self.responseAssert(apicase.expect, response)

        except Exception as e:
            # 方法内上抛异常，这里统一处理。提交BUG，错误数量 + 1，跳过本次执行
            print(e)
            self.submitBug(self.product, apicase.name, e)
            self.count_fail += 1
        else:
            self.count_pass += 1





from .models import Process, Step

class ProcessRun(RunApiCase):
    def __init__(self):
        self.product = Product.objects.get(productname='baidu')
    def run(self):
        # 1、获取某个产品的所有流程用例
        process_list = self.product.process.all()
        for process in process_list:

            # 提取参数保存变量,每次执行用例前初始化为空
            extract_param = {}

            # 1.2 获取用例的步骤
            step_list = Step.objects.filter(Process=process).all()
            for step in step_list:
                # 1.3 获取api
                api = step.api
                # 2、3 获取headers param
                try:
                    headers = self.initHeader(api.headers)
                    param = self.initParam(api.param)

                    method = api.method
                    url = "127.0.0.1:80" + api.path
                    response = self.requestEnum(method, url, headers, param).text

                    # 5、响应断言
                    self.responseAssert(api.expect, response)

                    # 提取参数
                    extract_param = self.extract(response, api.extract, extract_param)
                except Exception as e:
                    # 方法内上抛异常，这里统一处理。提交BUG，错误数量 + 1，跳过本次执行
                    print(e)
                    self.submitBug(self.product, process.name+api.name, e)
                    self.count_fail += 1
                else:
                    self.count_pass += 1

        # 6、提交结果
        self.submitResult(self.product)
