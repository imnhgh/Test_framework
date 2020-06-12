import yaml
import os

# 初始化一个YamlReader传入yml文件路径，用data函数获取load之后的list数据
class YamlReader:
    def __init__(self, yamlf):
        # 文件存在则调用，不存在抛出错误
        if os.path.exists(yamlf):
            self.yamlf = yamlf
        else:
            raise FileNotFoundError('文件不存在')
        self._data = None

    # 装饰器，将data方法转为属性直接调用返回self.data
    @property
    def data(self):
        # 第一次调用则读取yaml文档，否则返回之前的data
        if not self._data:
            with open(self.yamlf, 'rb') as f:
                self._data = list(yaml.safe_load_all(f))
        return self._data



if __name__ == "__main__":
    run_path = os.path.abspath('.')
    config_path = os.path.join(run_path, 'config/config.yml')

    reader = YamlReader(config_path)
    print(reader.data)

    