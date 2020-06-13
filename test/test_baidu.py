import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import unittest
# 导入自己的模块需要添加系统路径
import sys
sys.path.append(os.path.abspath('.'))
from utils.config import Config, DRIVER_PATH, DATA_PATH, REPORT_PATH
from utils.log import logger
from utils.file_reader import ExcelReader
from utils.HTMLTestRunner import HTMLTestRunner

class TestBaiDu(unittest.TestCase):
    # 配置分离 数据分离
    URL = Config().get('URL')
    excel = DATA_PATH + '/baidu.xlsx'

    locator_kw = (By.ID, 'kw')
    locator_su = (By.ID, 'su')
    locator_result = (By.XPATH, '//*[@id="content_left"]/div/h3/a')
    
    def sub_setUp(self):
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH + r'\chromedriver.exe')
        self.driver.get(self.URL)
    
    def sub_tearDown(self):
        self.driver.quit()

    def test_search(self):
        datas = ExcelReader(self.excel).data
        for d in datas:
            # 不用subtest的话某个用例判定出错则会退出，不去执行后面的
            # 相当于写了n个方法，每个方法测试一个数据
            # subTest没有setup和teardown，需要手动添加
            with self.subTest(data=d):
                logger.debug("test begin -> %s" % d['search'])
                self.sub_setUp()
                self.driver.find_element(*self.locator_kw).send_keys(d['search'])
                self.driver.find_element(*self.locator_su).click()
                sleep(2)  # 不sleep下面的results可能会获取不到元素

                results = self.driver.find_elements(*self.locator_result)
                logger.debug("results:{}".format(results))
                for r in results:
                    logger.info(r.get_attribute('href'))
                    logger.info(r.text)
                
                self.sub_tearDown()
                logger.debug("test end -> %s" % d['search'])





if __name__ == "__main__":
#     verbosity是一个选项,表示测试结果的信息复杂度，有0、1、2 三个值
# 0 (静默模式): 你只能获得总的测试用例数和总的结果 比如 总共10个 失败2 成功8
# 1 (默认模式): 非常类似静默模式 只是在每个成功的用例前面有个“.” 每个失败的用例前面有个 “F”
# 2 (详细模式):测试结果会显示每个测试用例的所有相关的信息
    #unittest.main(verbosity=2)
    report = os.path.join(REPORT_PATH, 'report.html')
    with open(report, 'wb') as f:
        runner = HTMLTestRunner(f, verbosity=2, title='TestFrame测试框架', description='修改html测试报告')
        runner.run(TestBaiDu('test_search'))

# 通过By和直接调用无差别
# driver.find_element_by_id('kw').send_keys("selenium")
# driver.find_element_by_id('su').click()
# results = driver.find_elements_by_xpath('//*[@id="content_left"]/div/h3/a')


