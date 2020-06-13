import yaml
import os
from xlrd import open_workbook # excel

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

# 自定义异常类
class SheetTypeError(Exception):
    pass

class ExcelReader:
    """
    读取excel文件中的内容。返回list。

    如：
    excel中内容为：
    | A  | B  | C  |
    | A1 | B1 | C1 |
    | A2 | B2 | C2 |

    如果 print(ExcelReader(excel, title_line=True).data)，输出结果：
    [{A: A1, B: B1, C:C1}, {A:A2, B:B2, C:C2}]

    如果 print(ExcelReader(excel, title_line=False).data)，输出结果：
    [[A,B,C], [A1,B1,C1], [A2,B2,C2]]

    可以指定sheet，通过index或者name：
    ExcelReader(excel, sheet=2)
    ExcelReader(excel, sheet='BaiDuTest')
    """
    def __init__(self, excel, sheet = 0, title_line = True):
        if not os.path.exists(excel):
            raise FileNotFoundError("excel file not found, path: %s" % excel)
        else:
            self.excel = excel
        self.sheet = sheet
        self.title_line = title_line
        self._data = list()  # 数据初始化为一个list

    @property
    def data(self):
        # data为空list则获取数据
        if not self._data:
            # 打开data excel
            workbook = open_workbook(self.excel)
            
            # 如果sheet名为数字则获取table_by_index
            # str则sheet_by_name
            if type(self.sheet) not in [int, str]:
                raise ValueError("excelReader.sheet must be int or str, but now is %s" % type(self.sheet))
            elif type(self.sheet) == int:
                s = workbook.sheet_by_index(self.sheet)
            elif type(self.sheet) == str:
                s = workbook.sheet_by_name(self.sheet)
            
            # 如果有标题栏
            if self.title_line:
                title = s.row_values(0)  # 首行为title
                for col in range(1, s.nrows):
                    # 通过zip函数将title和行值组成tuple再转为dict,用于可迭代对象
                    # dict(zip(iterable, iterable))常见用法
                    self._data.append(dict(zip(title, s.row_values(col))))
            else:
                # 无标题则直接添加至list[[v00, v01, v02], [v10, v11, v12]]
                # 相当于二维数组
                for col in range(s.nrows):
                    self._data.append(s.row_values(col))  # row_values(index) 返回一行的list
        return self._data



# TEST
def test_yamlReader():
    run_path = os.path.abspath('.')
    config_path = os.path.join(run_path, 'config/config.yml')
    reader = YamlReader(config_path)
    print(reader.data)

def test_excelReader():
    run_path = os.path.abspath('.')
    data_path = os.path.join(run_path, 'data/baidu.xlsx')
    print(data_path)
    reader = ExcelReader(data_path)
    print(reader.data)
    pass

if __name__ == "__main__":
    test_excelReader()
    