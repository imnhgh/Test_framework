# 读取配置

import os

# 导入自己的模块需要添加系统路径
import sys
sys.path.append(os.path.abspath('.'))

from utils.file_reader import YamlReader

BASE_PATH = os.path.split(os.path.dirname(os.path.abspath(__file__)))[0]
CONFIG_PATH = os.path.join(BASE_PATH, 'config', 'config.yml')
DATA_PATH = os.path.join(BASE_PATH, 'data')
DRIVER_PATH = os.path.join(BASE_PATH, 'drivers')
LOG_PATH = os.path.join(BASE_PATH, 'log')
REPORT_PATH = os.path.join(BASE_PATH, 'report')

class Config:
    def __init__(self, config = CONFIG_PATH):
        # 将YamlReader获得的list数据传给config
        self.config = YamlReader(config).data   
    
    def get(self, element, index = 0):
        #
        # yaml是可以通过'---'分节的。用YamlReader读取返回的是一个list，第一项是默认的节，如果有多个节，可以传入index来获取。
        # 这样我们其实可以把框架相关的配置放在默认节，其他的关于项目的配置放在其他节中。可以在框架中实现多个项目的测试。
        # 其实是list[index].get(key)  list[index]是dict
        return self.config[index].get(element)

if __name__ == '__main__':
    cfg = Config()  # 默认路径
    # 读取缩进的内容时要先获取其上一级例如log
    print(cfg.get('URL'))
    print(cfg.get('log').get('file_name'))


