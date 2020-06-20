# -*- coding: utf-8 -*-

import requests
from lxml import etree
from urllib.parse import quote
import time


class Book(object):

    def __init__(self):
        self.s_list = []
        self.a = 0

    def start(self, name):
        # 学霸的黑科技系统
        search_key = quote(name)
        # print(search_key)
        url = "https://m.37zw.net/s/so.php?type=articlename&s=" + search_key
        response = requests.get(url)
        if response.status_code == 200:
            content = response.content
            html = etree.HTML(content)
            book_list = html.xpath('//div[@class="cover"]/p[@class="line"]')
            book_list2 = []
            for book in book_list:
                b_name = book.xpath('./a[2]/text()')[0]
                b_class = book.xpath('./a[1]/text()')[0]
                b_id = book.xpath('./a[2]/@href')[0]
                b_author = book.xpath('./text()')[0]
                book_list2.append((book_name, b_id))
                print("搜索结果如下")
                print(b_class, b_name, b_id, b_author)
                print("")
            name = input("请从输入以上列表中的书籍名或输入NO退出:")
            if name == "NO" or name == "No" or name == "no" or name == "nO":
                return
            else:
                for b in book_list2:
                    if name == b[0]:
                        s_time = time.time()
                        for page in range(1, 50):
                            b_url = "https://m.37zw.net" + b[1] + "index_" + str(page) + ".html"
                            status = self.get_section(b_url)
                            if not status:
                                break
                        print(time.time() - s_time)
                        self.get_page()

    def get_page(self):
        for data in self.s_list:
            a, u, t = data
            print(a, t)
        start_s = int(input("开始章节:"))
        for s in self.s_list:
            a, u, t = s
            if a >= int(start_s):
                self.get_info(t, u)
                input("回车继续")

    def get_section(self, link):
        response = requests.get(link)
        if response.status_code == 200:
            content = response.content
            html = etree.HTML(content)
            section_list = html.xpath('//div[@class="cover"]/ul/li/a/@href')
            title_list = html.xpath('//div[@class="cover"]/ul/li/a/text()')
            for a in range(0, len(section_list)):
                self.a += 1
                self.s_list.append((self.a, section_list[a], title_list[a]))
            return True
        else:
            return False

    def get_info(self, title, link):
        link = "https://m.37zw.net" + link
        print(link)
        print(title)
        response = requests.get(link)
        if response.status_code == 200:
            content = response.content
            html = etree.HTML(content)
            body = html.xpath('//div[@id="nr1"]/text()')
            for b in body:
                print(b)


if __name__ == '__main__':
    # book_name = input("书籍名:")
    book_name = "网游之全民领主"
    book = Book()
    book.start(book_name)


