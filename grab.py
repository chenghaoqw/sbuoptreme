# coding:utf-8
import json
import ssl
from http import cookiejar
from urllib.parse import urlencode
from urllib.request import HTTPCookieProcessor, build_opener, Request

import sys

import time

index = 3
INFO_URL = "http://1.surpreme.applinzi.com/" + str(index)
STOCK_URL = "http://www.supremenewyork.com/mobile_stock.json?_="
SHOP_URL = "http://www.supremenewyork.com/shop/"
CHECKOUT_URL = "https://www.supremenewyork.com/checkout.json"
upload_file_name = index + time.time()

ssl._create_default_https_context = ssl._create_unverified_context


class netWork(object):
    COOKIE_NAME = "cookie"

    def __init__(self):
        try:
            self.cj = cookiejar.MozillaCookieJar(netWork.COOKIE_NAME)
            self.cj.load(netWork.COOKIE_NAME, ignore_discard=True, ignore_expires=True)
        except FileNotFoundError:
            print("cookie error")
        self.handler = HTTPCookieProcessor(self.cj)
        self.opener = build_opener(self.handler)

    def get_application_info(self):
        req = Request(INFO_URL, method="GET")
        response = self.opener.open(req)
        response = response.read().decode('utf-8')
        return json.loads(response)

    def get_stock(self):
        req = Request(STOCK_URL + str(int(time.time())), method="GET")
        req.add_header("User-Agent",
                       "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 MicroMessenger/6.5.9 NetType/WIFI Language/zh_CN")
        response = self.opener.open(req)
        response = response.read().decode('utf-8')
        return json.loads(response)['products_and_categories']

    def get_good_postdata(self, gid):
        req = Request(SHOP_URL + str(gid) + ".json", method="GET")
        response = self.opener.open(req)
        response = response.read().decode('utf-8')
        return json.loads(response)['styles']

    def add_good_cart(self, gid, post):
        headers = {
            # "Host": "www.supremenewyork.com",
            # "Proxy-Connection": "keep-alive",
            # "Origin": "http://www.supremenewyork.com",
            # "X-CSRF-Token": "ItGGEPpERDbLPHwptPxybPfyI9a8OgVs27p/ylDw0qp9UMbc3wdXM3KRESfO9BhHEBlcqOfVxF3bhELRrVNT+w==",
            # "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.186 Safari/537.36",
            # "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
            "Accept": "*/*;q=0.5, text/javascript, application/javascript, application/ecmascript, application/x-ecmascript",
            "X-Requested-With": "XMLHttpRequest",
            # "Referer": "http://www.supremenewyork.com/shop/accessories/qnhaqotsg",
            # "Accept-Encoding": "gzip, deflate",
        }
        req = Request(SHOP_URL + str(gid) + "/add", post.encode(encoding='UTF8'), headers=headers)
        response = self.opener.open(req)
        result = response.read().decode('utf-8')

    def check_out(self, post):
        req = Request(CHECKOUT_URL, post.encode(encoding='UTF8'))
        response = self.opener.open(req)
        return response.read().decode('utf-8')


'''_________________________________________________________________________'''


def start_bot():
    stock = net.get_stock()

    goods_usable = []
    for good_want in commit_info['goods']:
        in_categroy = stock[good_want['category']]
        for good in in_categroy:
            for good_one in good_want['name']:
                if good_one in good['name']:
                    goods_usable.append(good)

    goods_inventory = []
    for good_valid in goods_usable:
        for property_info in net.get_good_postdata(good_valid['id']):
            sizes = property_info['sizes']
            for size in sizes:
                if size['stock_level'] == 1:
                    post_dict = {
                        'utf8': '✓',
                        'style': property_info['id'],
                        'size': size['id'],
                        'commit': 'カートに入れる'
                    }
                    good_inventory = dict()
                    good_inventory['post_data'] = urlencode(post_dict)
                    good_inventory['id'] = good_valid['id']
                    goods_inventory.append(good_inventory)

    if not any(goods_inventory):  # no good can buy
        return

    for good_buy in goods_inventory:
        net.add_good_cart(good_buy['id'], good_buy['post_data'])

        result = net.check_out(commit_info['commit'])
        print(result)


'''_________________________________________________________________________'''

if __name__ == '__main__':
    net = netWork()
    commit_info = net.get_application_info()
    if not (any(commit_info) or commit_info['isValid'] != 1 or len(commit_info['goods']) == 0):
        sys.exit()
    start_bot()
