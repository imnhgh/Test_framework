import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from time import sleep
import unittest
# 导入自己的模块需要添加系统路径
import sys
sys.path.append(os.path.abspath('.'))
from utils.config import Config, DRIVER_PATH
from utils.log import logger

class TestBaiDu(unittest.TestCase):
    # 配置分离
    URL = Config().get('URL')

    locator_kw = (By.ID, 'kw')
    locator_su = (By.ID, 'su')
    locator_result = (By.XPATH, '//*[@id="content_left"]/div/h3/a')
    
    def setUp(self):
        self.driver = webdriver.Chrome(executable_path=DRIVER_PATH + r'\chromedriver.exe')
        self.driver.get(self.URL)
    
    def tearDown(self):
        self.driver.quit()

    def test_search_0(self):
        self.driver.find_element(*self.locator_kw).send_keys("selenium")
        self.driver.find_element(*self.locator_su).click()
        sleep(2)
        results = self.driver.find_elements(*self.locator_result)
        for r in results:
            logger.info(r.get_attribute('href'))
            logger.info(r.text)

    def test_search_1(self):
        self.driver.find_element(*self.locator_kw).send_keys("python")
        self.driver.find_element(*self.locator_su).click()
        sleep(2)
        results = self.driver.find_elements(*self.locator_result)
        for r in results:
            logger.info(r.get_attribute('href'))
            logger.info(r.text)

if __name__ == "__main__":
    unittest.main()


# 通过By和直接调用无差别
# driver.find_element_by_id('kw').send_keys("selenium")
# driver.find_element_by_id('su').click()
# results = driver.find_elements_by_xpath('//*[@id="content_left"]/div/h3/a')


