# This package will contain the spiders of your Scrapy project
#
# Please refer to the documentation for information on how to create and manage
# your spiders.
import re
az_dict = {
        '0': 'A', '1': 'B', '2': 'C', '3': 'D', '4': 'E',
        '5': 'F', '6': 'G', '7': 'H', '8': 'I', '9': 'J',
        '10': 'K', '11': 'L', '12': 'M', '13': 'N', '14': 'O',
        '15': 'P', '16': 'Q', '17': 'R', '18': 'S', '19': 'T',
        '20': 'U', '21': 'V', '22': 'W', '23': 'X', '24': 'Y',
        '25': 'Z'
    }

if __name__ == '__main__':
    print(''.join('aaa啊啊啊', '111'))
    # url = "https://car.autohome.com.cn/AsLeftMenu/As_LeftListNew.ashx?typeId=1 &brandId=%d &fctId=0 &seriesId=0"
    # url = (url % '117')
    # print(url)
    # pattern = re.compile(r'(?<=-).*?(?=\.)')
    # str = '/price/brand-117.html'
    #
    # print(str(pattern.findall(str)))
    #
    #
    # print(az_dict['0'])
    # print(az_dict)