# coding:utf-8
import json
import re
import ssl
import requests
from urllib.parse import urlencode, quote

import sys

import time

index = 3
INFO_URL = "http://1.surpreme.applinzi.com/" + str(index)
STOCK_URL = "http://www.supremenewyork.com/mobile_stock.json?_="
SHOP_URL = "http://www.supremenewyork.com/shop/"
PRE_CHECKOUT_URL = "https://www.supremenewyork.com/checkout"
CHECKOUT_URL = "https://www.supremenewyork.com/checkout.json"
upload_file_name = index + time.time()

ssl._create_default_https_context = ssl._create_unverified_context


class netWork(object):
    COOKIE_NAME = "cookie"

    def __init__(self):
        self.http = requests.Session()

    def get_application_info(self):
        # req = self.http.request( method="GET", url=INFO_URL)
        response = self.http.post(INFO_URL)
        response = response.content.decode('utf-8')
        return json.loads(response)

    def get_stock(self):
        response = self.http.get(STOCK_URL + str(int(time.time())))
        response = response.content.decode('utf-8')
        return json.loads(response)['products_and_categories']

    def get_good_postdata(self, gid):
        response = self.http.get(SHOP_URL + str(gid) + ".json")
        return response.json()['styles']

    def add_good_cart(self, good):
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
        response = self.http.post(SHOP_URL + str(good['id']) + "/add", data=good['post_data'].encode(encoding='UTF8'),
                                  headers=headers)
        result = response.content.decode('utf-8')
        pure_cart = json.loads(re.findall(r'var h = (.+?);', result)[0])
        pure_cart["total"] = "¥" + str(good['price'] / 100)
        pure_cart = str(pure_cart)
        pure_cart_string = quote(pure_cart)
        self.http.cookies.set("pure_cart",
                              "%7B%2250483%22%3A1%2C%22cookie%22%3A%221%20item--50483%2C18271%22%2C%22total%22%3A%22%C2%A58100%22%7D")

    def pre_checkout(self):
        response = self.http.get(PRE_CHECKOUT_URL, verify=False)
        response = response.content.decode('utf-8')
        return quote(re.findall(r'<meta name="csrf-token" content="(.+?)"', response)[0])

    def check_out(self, post):
        headers = {
            "cache-control": "max-age=0",
            "origin": "https://www.supremenewyork.com",
            "upgrade-insecure-requests": "1",
            "content-type": "application/x-www-form-urlencoded",
            "user-agent": "Mozilla/5.0(Macintosh;Intel Mac OS X10_11_6) AppleWebKit / 537.36(KHTML, likeGecko) Chrome/64.0.3282.186 Safari/537.36",
            "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            "referer": "https://www.supremenewyork.com/checkout",
            "accept-encoding": "gzip,deflate,br",
            "accept-language": "zh-CN,zh;q=0.9,en;q=0.8"}
        response = self.http.post(CHECKOUT_URL, data=post, verify=False, headers=headers)
        return response.content.decode('utf-8')


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
                    good_inventory['price'] = good_valid['price']
                    goods_inventory.append(good_inventory)

    if not any(goods_inventory):  # no good can buy
        return

    for good_buy in goods_inventory:
        net.add_good_cart(good_buy)

    post_data = {
        "utf8": "✓",
        "authenticity_token": "FUA3TiMFmPJ26w0YRHnaap77ydT3NSMRtJ7jvaOp3ZI1h78il6qslIzexw7LxhZe3tpWUC5SUNi7 / cw1DV + mow ==",
        "credit_card[last_name]": "hu",
        "credit_card[first_name]": "yang",
        "order[email]": "h924429615@gmail.com",
        "order[tel]": "09012592053",
        "order[billing_state]": "東京都",
        "order[billing_city]": "东京",
        "order[billing_address]": "東京都豊島区南大塚1 - 51 - 9",
        "order[billing_zip]": "173-0005",
        "same_as_billing_address": "1",
        "credit_card[type]": "cod",
        "credit_card[cnb]": "",
        "credit_card[month]": "03",
        "credit_card[year]": "2018",
        "credit_card[vval]": "",
        "order[terms]": "0",
        "order[terms]": "1",
        "hpcvv": "",
        "commit": "購入する"
    }
    token = net.pre_checkout()
    post_data = "utf8=%E2%9C%93&authenticity_token=0kQsJ4HPpS348Y%2FbiFH3K2msSnxA%2Bw4WxJFQaMFtIIcsVoy7r8HLJpabg68keePX3ogs0LeGKvqnyTX9bzXExQ%3D%3D&credit_card%5Blast_name%5D=hu&credit_card%5Bfirst_name%5D=yang&order%5Bemail%5D=h924429615%40gmail.com&order%5Btel%5D=09012592053&order%5Bbilling_state%5D=+%E6%9D%B1%E4%BA%AC%E9%83%BD&order%5Bbilling_city%5D=%E6%9D%B1%E4%BA%AC%E9%83%BD%E8%B1%8A%E5%B3%B6%E5%8C%BA%E5%8D%97%E5%A4%A7%E5%A1%9A1-51-9&order%5Bbilling_address%5D=%E8%97%A4%E5%92%8C%E5%8D%97%E5%A4%A7%E5%A1%9A+501&order%5Bbilling_zip%5D=173-0005&same_as_billing_address=1&credit_card%5Btype%5D=cod&credit_card%5Bcnb%5D=&credit_card%5Bmonth%5D=03&credit_card%5Byear%5D=2018&credit_card%5Bvval%5D=&order%5Bterms%5D=0&order%5Bterms%5D=1&hpcvv=&commit=%E8%B3%BC%E5%85%A5%E3%81%99%E3%82%8B"
    pattern = 'authenticity_token=(.*?)&'
    post_data = re.sub(pattern, "authenticity_token=" + token + "&", post_data)
    result = net.check_out(post_data)
    print(result)


'''_________________________________________________________________________'''

if __name__ == '__main__':
    net = netWork()
    commit_info = net.get_application_info()
    if not (any(commit_info) or commit_info['isValid'] != 1 or len(commit_info['goods']) == 0):
        sys.exit()
    start_bot()
