from product.models import Product
import requests


class ApiCaseRun():
    def run(self):
        count_pass = 0
        count_fail = 0

        # 1、获取某个产品的所有用例，返回数据可迭代
        apis = Product.objects.get(productname='baidu').apis.all()
        for api in apis:

            # 2、3 获取headers param
            try:
                headers = self.initHeader(api.headers)
                param = self.initParam(api.param)
            except:
                # 如果headers param 格式不正确导致异常，则提交BUG，错误数量+1，跳过本次执行
                self.submitBug("headers|param erro")
                count_fail = count_fail + 1
                continue

            # 4、发出请求
            method = api.method
            url = "127.0.0.1:80" + api.path
            try:
                response = self.requestEnum(method, url, headers, param).text
            except:
                self.submitBug("requst erro")
                count_fail = count_fail + 1
                continue

            # 5、响应断言
            if self.responseAssert(api.expected, response):
                self.submitBug("expected erro")
                count_fail = count_fail + 1
                continue

        # 6、提交结果
        self.submitResult('baidu', count_pass, count_fail)
        return "pass:{}, fail:{}".format(count_pass, count_fail)


    def requestEnum(self, method, url, headers, param):
        if method == 'get':
            return requests.get(url, data=param, headers=headers)
        elif method == 'post':
            return requests.post(url, data=param, headers=headers)

    # 处理数据
    def initHeader(self, headers):
        return headers

    # 处理数据
    def initParam(self, param):
        return param

    # 提交BUG
    def submitBug(self, data):
        pass

    # 响应断言
    def responseAssert(self, expected, response):
        return expected not in response

    # 提交结果统计
    def submitResult(self, product, count_pass, count_fail):
        pass


from product.models import Product
from .models import Process, Step
import requests


class ProcessRun():
    def run(self):
        count_pass = 0
        count_fail = 0

        # 1、获取某个产品的所有流程用例
        process_list = Product.objects.get(productname='baidu').process.all()
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
                except:
                    # 如果headers param 格式不正确导致异常，则提交BUG，错误数量+1，跳过本次执行
                    self.submitBug("headers|param erro")
                    count_fail = count_fail + 1
                    break  # 如果执行失败了，结束本用例

                    # 4、发出请求
                method = api.method
                url = "127.0.0.1:80" + api.path
                try:
                    response = self.requestEnum(method, url, headers, param).text
                except:
                    self.submitBug("requst erro")
                    count_fail = count_fail + 1
                    break

                # 5、响应断言
                if self.responseAssert(api.expect, response):
                    self.submitBug("expect erro")
                    count_fail = count_fail + 1
                    break

                # 提取参数
                try:
                    extract_param =  self.extract(api.extract,response)
                except:
                    self.submitBug("extract erro")
                    count_fail = count_fail + 1
                    break
        # 6、提交结果
        self.submitResult('baidu', count_pass, count_fail)


    def requestEnum(self, method, url, headers, param):
        if method == 'get':
            return requests.get(url, data=param, headers=headers)
        elif method == 'post':
            return requests.post(url, data=param, headers=headers)


    # 处理数据
    def initHeader(self, headers):
        return headers


    # 处理数据
    def initParam(self, param):
        return param


    # 提交BUG
    def submitBug(self, data):
        pass


    # 响应断言
    def responseAssert(self, expect, response):
        return expect not in response

    # 从响应内容提取参数
    def extract(self, extract, response):
         pass


    # 提交结果统计
    def submitResult(self, product, count_pass, count_fail):
        pass
