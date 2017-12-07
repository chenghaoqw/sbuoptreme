#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# version:0.0.1
import json
from http import cookiejar
from urllib.request import HTTPCookieProcessor, build_opener, Request

import time

import sys

baidu = "https://www.baidu.com"
goods1 = 'http://www.supremenewyork.com/shop/4437/add'
goods2 = 'http://www.supremenewyork.com/shop/4632/add'
post_data1 = "utf8=%E2%9C%93&style=16668&size=45067&commit=%E3%82%AB%E3%83%BC%E3%83%88%E3%81%AB%E5%85%A5%E3%82%8C%E3%82%8B"
post_data2 = "utf8=%E2%9C%93&style=17486&size=48019&commit=%E3%82%AB%E3%83%BC%E3%83%88%E3%81%AB%E5%85%A5%E3%82%8C%E3%82%8B"
cart = 'http://www.supremenewyork.com/shop/cart'
checkout = 'https://www.supremenewyork.com/checkout'
check_post = "utf8=%E2%9C%93&authenticity_token=C5yjONx%2FOI5G%2FTGuLAO%2BEPB14vjOfxe7jOr5B%2FvmK5JGATFTIahelu18RlEMjBRm%2BZQy%2BOE9CGTVunAGNN2N%2FA%3D%3D&credit_card%5Blast_name%5D=hu&credit_card%5Bfirst_name%5D=yang&order%5Bemail%5D=h924429615@gmail.com&order%5Btel%5D=09012592053&order%5Bbilling_state%5D=+%E6%9D%B1%E4%BA%AC%E9%83%BD&order%5Bbilling_city%5D=%E4%B8%9C%E4%BA%AC&order%5Bbilling_address%5D=%E6%9D%BF%E6%A9%8B%E5%8C%BA%E5%A4%A7%E8%B0%B7%E5%8F%A3%E5%8C%97%E7%94%BA18-3&order%5Bbilling_zip%5D=173-0031&same_as_billing_address=1&credit_card%5Btype%5D=cod&credit_card%5Bcnb%5D=4033920041674989&credit_card%5Bmonth%5D=11&credit_card%5Byear%5D=2022&credit_card%5Bvval%5D=909&order%5Bterms%5D=0&order%5Bterms%5D=1&hpcvv=&commit=%E8%B3%BC%E5%85%A5%E3%81%99%E3%82%8B"
has_cookie = False
file_name = "cookie"
stock = "http://www.supremenewyork.com/mobile_stock.json?_="
property = "http://www.supremenewyork.com/shop/"
info = "http://1.surpreme.applinzi.com/"
goods_info = ""


# ssl._create_default_https_context = ssl._create_unverified_context

class shop(object):
    def __init__(self):
        self.cj = cookiejar.MozillaCookieJar(file_name)
        if (has_cookie):
            self.cj.load(file_name, ignore_discard=True, ignore_expires=True)
        self.handler = HTTPCookieProcessor(self.cj)
        self.opener = build_opener(self.handler)

    def getInfo(self):
        url = info
        req = Request(url, method="GET")
        response = self.opener.open(req)
        response = response.read().decode('utf-8')
        return response

    def getGoods(self):
        url = stock + str(int(time.time()))
        req = Request(url, method="GET")
        req.add_header("User-Agent",
                       "Mozilla/5.0 (Linux;U;Android 2.3;en-us;Nexus One Build/FRF91)AppleWebKit/999+(KHTML, like Gecko)Version/4.0 Mobile Safari/999.9")
        response = self.opener.open(req)
        response = response.read().decode('utf-8')
        print(response)
        j = json.loads(response)['products_and_categories']
        for i in j:
            print(i)
            for k in j[i]:
                name = k['name']
                print(k)
                # if 'The North Face' in name and 'Tee' in name:
                #     print(k)


    def getProperty(self, id):
        url = property + str(id) + ".json"
        print(url)
        req = Request(url, method="GET")
        response = self.opener.open(req)
        response = response.read().decode('utf-8')
        j = json.loads(response)['styles']
        for i in j:
            print(i)
            # j = json.loads(response)['products_and_categories']
            # for i in j:
            #     print(i)
            #     for k in j[i]:
            #         name = k['name']
            #         if 'The North Face' in name and 'Tee' in name:
            #             print(k)

    def add_good(self, url, post):
        # post_data = urllib.urlencode(post)
        req = Request(url, post.encode(encoding='UTF8'))
        response = self.opener.open(req)
        for item in self.cj:
            print('Name = ' + item.name)
            print('Value = ' + item.value)
        print("")
        self.cj.save(ignore_discard=True, ignore_expires=True)
        has_cookie = True
        # print response.read()

    def checkout(self, url, post):
        # post_data = urllib.urlencode(post)
        req = Request(url, post.encode(encoding='UTF8'))
        response = self.opener.open(req)
        self.cj.save(ignore_discard=True, ignore_expires=True)
        has_cookie = True
        for item in self.cj:
            print('Name = ' + item.name)
            print('Value = ' + item.value)
        print("")
        print(response.read().decode('utf-8'))


if __name__ == '__main__':
    cls_shop = shop()
    response = cls_shop.getInfo()
    j = json.loads(response)
    if (response['isValid'] != 1):
        sys.exit()
    goods_info = response['goods']
    cls_shop.getGoods()
    cls_shop.getProperty(4686)
    cls_shop.add_good(goods1, post_data1)
    cls_shop.add_good(goods2, post_data2)
    cls_shop.checkout(checkout, check_post)
