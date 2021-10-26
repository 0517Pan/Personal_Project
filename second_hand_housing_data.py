"""
Author : Pan
Data : 2021/10/25 19:13
Tool : PyCharm
Title: 爬取链家二手房房源信息
"""
import requests
import bs4
import csv

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) \
                  Chrome/92.0.4515.159 Safari/537.36 Edg/92.0.902.78'
}

# 爬取房源的房源地
address = {'cd': '成都', 'sn': '遂宁', 'pzh': '攀枝花', 'dy': '德阳', 'mianyang': '绵阳',
           'guangyuan': '广元', 'leshan': '乐山', 'nanchong': '南充', 'ms': '绵山',
           'yibin': '宜宾', 'dazhou': '达州', 'yaan': '雅安', 'liangshan': '凉山'}

# 写入csv文件中
with open(r'C:\Users\28102\Desktop\成都二手房.csv', 'a', encoding = 'utf-8') as f:
    csv_writer = csv.writer(f)
    # 写入表头
    csv_writer.writerow(['区域', '标题', '总价', '单价', '位置', '信息'])
    for ad in address.keys():
        # 存储房源信息
        message = []
        # 爬取100页房源信息
        for i in range(1, 101):
            url = f'https://{ad}.lianjia.com/ershoufang/pg{i}'
            # 获取响应
            resp = requests.get(url = url, headers = headers)
            # 设置解析器，解析响应内容
            soup = bs4.BeautifulSoup(resp.text, 'html.parser')
            # 共同标签段
            li_list = soup.select('#content > div.leftContent > ul > li')
            # 需要获取的标签内容
            tag = ['title> a', 'priceInfo>.totalPrice', 'priceInfo>.unitPrice', 'flood> .positionInfo',
                   'address>.houseInfo']
            for j in li_list:
                message_demo = [address[ad]]
                for t in tag:
                    msg = j.select_one(f'li> .info>.{t}')
                    # 若标签内容不为None，则放入列表中
                    if msg != None:
                        message_demo.append(msg.text)
                message.append(message_demo)
        # 将列表中房源信息写入csv文件中
        for k in message:
            csv_writer.writerow(k)
