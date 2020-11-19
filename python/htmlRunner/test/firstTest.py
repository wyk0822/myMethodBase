import time

from HtmlTestRunner import HTMLTestRunner
import os, sys, unittest


class TestRunner(object):
    ''' Run test '''

    def __init__(self, cases="./", title=u'自动化测试报告', description=u'环境：windows 7'):
        self.cases = cases
        self.title = title
        self.des = description

    def run(self):

        for filename in os.listdir(self.cases):
            if filename == "report":
                break
        else:
            os.mkdir(self.cases + '/report')

        now = time.strftime("%Y-%m-%d_%H_%M_%S")
        fp = open("./report/" + now + "result.html", 'wb')
        tests = unittest.defaultTestLoader.discover("../test_case", pattern='*sta.py', top_level_dir=None)
        runner = HTMLTestRunner(stream=fp, title=self.title, description=self.des)
        runner.run(tests)
        fp.close()

    def debug(self):
        tests = unittest.defaultTestLoader.discover(self.cases, pattern='*sta.py', top_level_dir=None)
        runner = unittest.TextTestRunner()
        runner.run(tests)


if __name__ == '__main__':
    test = TestRunner()
    test.run()
