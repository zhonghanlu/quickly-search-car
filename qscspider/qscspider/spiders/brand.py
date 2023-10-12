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
        '0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E',
        '5': 'F', '6': 'G', '7': 'H', '8': 'I', '9': 'J',
        '10': 'K', '11': 'L', '12': 'M', '13': 'N', '14': 'O',
        '15': 'P', '16': 'Q', '17': 'R', '18': 'S', '19': 'T',
        '20': 'U', '21': 'V', '22': 'W', '23': 'X', '24': 'Y',
        '25': 'Z'
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
        for index in range(1):
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
                xpath_detail_url = ("//ul[%d]/li[%d]/dl/dt" % (index + 1, key + 1))

                yield scrapy.Request(url=self.start_urls[0] % brand_id,
                                     callback=lambda response, item=item, xpath_detail_url=xpath_detail_url:
                                     self.detail_parse(response, item, xpath_detail_url))

    def detail_parse(self, response, item, xpath_detail_url):
        detail_data = response.xpath(xpath_detail_url)
        for dt in detail_data:
            car_categorize = dt.xpath("./a/text()").extract_first()
            series_id = dt.xpath("./a/@href").extract_first()
            pattern = re.compile(r'(?<=-).*?(?=\.)')
            series_id = pattern.findall(series_id)[0]
            item["categorize"] = '^'.join((car_categorize, series_id))

            xpath_name_url = str(xpath_detail_url).replace("dt", "dd")
            name_data = response.xpath(xpath_name_url)
            for dd in name_data:
                car_name = dd.xpath("./a/text()").extract_first()
                series_id = dd.xpath("./a/@href").extract_first()
                pattern = re.compile(r'(?<=-).*?(?=\.)')
                series_id = pattern.findall(series_id)[0]
                item["name"] = '^'.join((car_name, series_id))
                yield item
