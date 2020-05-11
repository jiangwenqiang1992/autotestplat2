import time

from selenium import webdriver

from product.models import Product
from webtest.models import CaseStep, Case
from webtest.util.mydriver import MyWebDriver


class RunCase():

    driver = None
    def run(self):
        cases = Product.objects.get(name='官网').case.all()
        print(cases)

        for case in cases:
            self.startChrome()
            if case.pre_case:
                pre_case = Case.objects.get(casename=case.pre_case)
                steps = CaseStep.objects.filter(case=pre_case).all()
                self.runStep(steps)

            steps = CaseStep.objects.filter(case=case).all()
            self.runStep(steps)
            self.quitChrome()


    def startChrome(self):
        options = webdriver.ChromeOptions()
        options.add_argument(r'--user-data-dir=C:\Users\HP\AppData\Local\Google\Chrome\User Data')

        driver = webdriver.Chrome(chrome_options=options)  # 创建Chrome对象.

        # driver = webdriver.Chrome()  # 创建Chrome对象.
        # driver = webdriver.Firefox()
        driver.maximize_window()

        # driver.find_element_by_id('')
        driver.get('https://www.waykichain.com')
        self.driver = driver

    def quitChrome(self):
        time.sleep(2)
        self.driver.quit()

    def runStep(self, steps):
        for step in steps:
            time.sleep(1.5)
            element = step.element
            target = element.targeting
            target_value = element.value
            action = step.action
            action_value = step.value
            print(element.elementname, target, target_value, action, action_value)
            MyWebDriver(self.driver).TargetEnum(target, target_value).actionEnum(action, action_value)