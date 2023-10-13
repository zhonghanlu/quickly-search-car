import time

import scrapy
import re

from qscspider.items import BrandItem


class BrandSpider(scrapy.Spider):
    name = "brand"
    allowed_domains = ["car.autohome.com.cn"]
    start_urls = [
        "https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1 &brandId=%d &fctId=0 &seriesId=0"]

    # A-Z 字典
    az_dict = {
        '0': 'A', '1': 'B', '2': 'C', '3': 'D',
        # '4': 'E',
        '4': 'F', '5': 'G', '6': 'H', '7': 'I', '8': 'J',
        '9': 'K', '10': 'L', '11': 'M', '12': 'N', '13': 'O',
        '14': 'P', '15': 'Q', '16': 'R', '17': 'S', '18': 'T',
        # '20': 'U',
        # '19': 'V',
        '19': 'W', '20': 'X', '21': 'Y', '22': 'Z'
    }

    '''
     举例：
     汽车之家的数据都是静态页面数据
     A开头的汽车
     1.start_urls  仅可以获取车品牌
     2.请求第二次获取具体型号
     3.请求第三次获取具体详情
        类似于下列地址样式
    ?typeId=1 &brandId=0 &fctId=0 &seriesId=0
    ?typeId=1 &brandId=117 &fctId=0 &seriesId=0
    构建此次爬取的数据结构(采用csv形式)
    ["start":"A","categorize":"埃安","name":"埃安 S"]
    '''

    def start_requests(self):
        url = self.start_urls[0] % 0
        yield scrapy.Request(url)

    def parse(self, response):
        for index in range(23):
            time.sleep(0.3)
            xpath_rule = ("//ul[%d]/li" % (index + 1))

            brand_data = response.xpath(xpath_rule)

            # 从 1 开始为 A
            for key, li_data in enumerate(brand_data):
                item = BrandItem()
                # brandId  获取-之后.之前
                pattern = re.compile(r'(?<=-).*?(?=\.)')
                brand_id = li_data.xpath("./h3/a/@href").extract_first()
                brand_id = int(pattern.findall(brand_id)[0])

                item["start"] = self.az_dict[str(index)]
                item["brand"] = li_data.xpath("./h3/a/text()").extract_first()
                # 获取此分类下所有车系
                xpath_detail_url = ("//ul[%d]/li[%d]/dl/child::*" % (index + 1, key + 1))

                yield scrapy.Request(url=self.start_urls[0] % brand_id,
                                     callback=lambda response, item=item, xpath_detail_url=xpath_detail_url:
                                     self.detail_parse(response, item, xpath_detail_url))

    def detail_parse(self, response, item, xpath_detail_url):
        detail_data = response.xpath(xpath_detail_url)

        for node in detail_data:
            if node.xpath('self::dt'):
                car_categorize = node.xpath("./a/text()").extract_first()
                series_id = node.xpath("./a/@href").extract_first()
                pattern = re.compile(r'(?<=-).*?(?=\.)')
                series_id = pattern.findall(series_id)[0]
                item["categorize"] = '^'.join((car_categorize, series_id))
                # item["categorize"] = node.xpath('string(.)').get().strip()
                values_list = []
                # If the node is a <dd>, add its text to the current values_list
            elif node.xpath('self::dd'):
                car_name = node.xpath("./a/text()").extract_first()
                series_id = node.xpath("./a/@href").extract_first()
                pattern = re.compile(r'(?<=-).*?(?=\.)')
                series_id = pattern.findall(series_id)[0]
                values_list.append('^'.join((car_name, series_id)))
                # values_list.append(node.xpath('string(.)').get().strip())
                # If the next node is a <dt> or there are no more nodes, yield the item
            if node.xpath('following-sibling::*[1]/self::dt') or not node.xpath('following-sibling::*'):
                item["name"] = values_list
                yield item

        # for dt in detail_data:
        #     car_categorize = dt.xpath("./a/text()").extract_first()
        #     series_id = dt.xpath("./a/@href").extract_first()
        #     pattern = re.compile(r'(?<=-).*?(?=\.)')
        #     series_id = pattern.findall(series_id)[0]
        #     item["categorize"] = '^'.join((car_categorize, series_id))
        #
        #     xpath_name_url = str(xpath_detail_url).replace("dt", "dd")
        #     name_data = dt.xpath("following-sibling::dd")
        #     for dd in name_data:
        #         car_name = dd.xpath("./a/text()").extract_first()
        #         series_id = dd.xpath("./a/@href").extract_first()
        #         pattern = re.compile(r'(?<=-).*?(?=\.)')
        #         series_id = pattern.findall(series_id)[0]
        #         item["name"] = '^'.join((car_name, series_id))
        #         yield item
