from webtest.util import Click


class MyWebDriver():
    driver = None

    def __init__(self, driver):
        self.driver = driver

    def TargetEnum(self, num, value):
        element = None
        if num == '0':
            return self.by_coordinate(value)
        elif num == '1':
            element = self.driver.find_element_by_id(value)
        elif num == '2':
            element = self.driver.find_element_by_name(value)
        elif num == '3':
            element = self.driver.find_element_by_class_name(value)
        elif num == '4':
            element = self.driver.find_element_by_link_text(value)
        elif num == '5':
            element = self.driver.find_element_by_tag_name(value)
        elif num == '6':
            element = self.driver.find_element_by_css_selector(value)
        elif num == '7':
            element = self.driver.find_element_by_xpath(value)
        return self.MyElement(element)

    class CoordinateElement():
        __x = 0
        __y = 0

        def __init__(self, x, y):
            self.__x = x
            self.__y = y

        def actionEnum(self, num, value=None):
            if num == '1':
                self.click()
            elif num == '2':
                self.sendstr(value)
            elif num == '3':
                self.moveto()

        def click(self):
            Click.mouse_click(self.__x, self.__y)

        def sendstr(self, string):
            self.click()
            Click.sendString(string)

        def moveto(self):
            pass

        def __str__(self):
            return self.__x + self.__y

    def by_coordinate(self, coordinate):
        x, y = str(coordinate).split(',')
        return self.CoordinateElement(x, y)

    class MyElement():
        def __init__(self, element):
            self.element = element

        def actionEnum(self, num, value=None):
            if num == '1':
                self.click()
            elif num == '2':
                self.sendstr(value)
            elif num == '3':
                self.moveto()

        def click(self):
            self.element.click()

        def sendstr(self, str):
            self.element.send_keys(str)

        def moveto(self):
            ActionChains(MyWebDriver.driver).move_to_element(self.element)
