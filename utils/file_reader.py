import yaml
import os

class YamlReader:
    def __init__(self, yamlf):
        # 文件存在则调用，不存在抛出错误
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError('文件不存在')
        self._data = None

    @property
    def data(self):
        # 第一次调用则读取yaml文档，否则返回之前的data
        if not self._data:
            with open(self.yamlf, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))
        return self._data