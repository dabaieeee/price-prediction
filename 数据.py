import requests
from lxml import etree
# from pprint import pprint
import time
import csv
import numpy as np

"""
东方财富网
"""

stock = input("请输入期货代码:")
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36 Edg/109.0.1518.61'
}

# 爬虫主程序
def get_data(start, end):
    count = 1
    data = []
    for page in range(start, end+1):     # 爬取total_page页数据
        url = f"http://guba.eastmoney.com/list,{str(stock)},f_{str(page)}.html"
        resp = requests.get(url=url, headers=headers)
        resp.encoding = "utf-8"
        resp.close()
        # pprint(resp.text)
        html = etree.HTML(resp.text)

        divs = html.xpath('/html/body/div[6]/div[2]/div[4]/div')
        # print(len(divs))
        try:
            for div in divs[1:]:
                child_data = {}
                readers_num = div.xpath("./span[1]/text()")[0]
                comments_num = div.xpath("./span[2]/text()")[0]
                title = div.xpath("./span[3]/a/@title")[0]
                author = div.xpath("./span[4]/a/font/text()")[0]
                date = div.xpath("./span[5]/text()")[0]
                # 写入字典
                child_data["count"] = count
                child_data["readers_num"] = readers_num
                child_data["comments_num"] = comments_num
                child_data["title"] = title
                child_data["author"] = author
                child_data["date"] = date
                data.append(child_data)
                # print(count, readers_num, comments_num, title, author, date)
                count += 1
                # 睡眠
                time_ = np.random.random()
                if time_ > 0.4:
                    time_ = time_ / 10.5
                time.sleep(time_)
        except IndexError:
            print(f"第{page}页爬取完毕")
            continue
    return data

# 将数据写入csv文件
def write_data(data):
    headers = ("count", "readers_num", "comments_num", "title", "author", "date")
    with open(f'{str(stock)}.csv', 'w', encoding='utf-8-sig', newline='') as f:
        DictWriter = csv.DictWriter(f,headers)
        DictWriter.writeheader()
        DictWriter.writerows(data)
    print(f"期货{stock}爬取完毕")

if __name__ == '__main__':
    start_page = 1
    end_page = 2
    data = get_data(start_page, end_page)
    write_data(data)
