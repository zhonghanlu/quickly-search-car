# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html
import json

# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


class QscspiderPipeline:
    def process_item(self, item, spider):
        return item



class BrandPipeline(object):

    def __init__(self):
        self.file = open('car_brand.json', 'w', encoding='utf-8')

    def process_item(self, item, spider):
        # 将item对象强制转为字典，该操作只能在scrapy中使用
        item = dict(item)
        # 爬虫文件中提取数据的方法每yield一次，就会运行一次
        # 该方法为固定名称函数
        # 默认使用完管道，需要将数据返回给引擎
        # 1.将字典数据序列化
        '''ensure_ascii=False 将unicode类型转化为str类型，默认为True'''
        json_data = json.dumps(item, ensure_ascii=False, indent=2) + ',\n'

        # 2.将数据写入文件
        self.file.write(json_data)

        return item

    def __del__(self):
        self.file.close()