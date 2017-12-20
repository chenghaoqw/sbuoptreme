#!/usr/bin/env python
# _*_ coding:utf-8 _*_
# version:0.0.1
import json
import os
import re
import sched
from http import cookiejar
from http.cookiejar import Cookie
from urllib import request

from urllib.parse import urlencode
from urllib.parse import quote
from urllib.request import HTTPCookieProcessor, build_opener, Request

import datetime
from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.triggers.cron import CronTrigger
import datetime
import time
import ssl
import requests

ssl._create_default_https_context = ssl._create_unverified_context

import sys

index = '1'
starttime = ""
supreme_url = "http://www.supremenewyork.com"
supreme_shop_url = "http://www.supremenewyork.com/shop"
goodsurl = "http://www.supremenewyork.com/shop/"
cart = 'http://www.supremenewyork.com/shop/cart'
checkout_url = 'https://www.supremenewyork.com/checkout'
checkout_json__url = 'https://www.supremenewyork.com/checkout.json'
check_post = "utf8=%E2%9C%93&authenticity_token=C5yjONx%2FOI5G%2FTGuLAO%2BEPB14vjOfxe7jOr5B%2FvmK5JGATFTIahelu18RlEMjBRm%2BZQy%2BOE9CGTVunAGNN2N%2FA%3D%3D&credit_card%5Blast_name%5D=hu&credit_card%5Bfirst_name%5D=yang&order%5Bemail%5D=h924429615@gmail.com&order%5Btel%5D=09012592053&order%5Bbilling_state%5D=+%E6%9D%B1%E4%BA%AC%E9%83%BD&order%5Bbilling_city%5D=%E4%B8%9C%E4%BA%AC&order%5Bbilling_address%5D=%E6%9D%BF%E6%A9%8B%E5%8C%BA%E5%A4%A7%E8%B0%B7%E5%8F%A3%E5%8C%97%E7%94%BA18-3&order%5Bbilling_zip%5D=173-0031&same_as_billing_address=1&credit_card%5Btype%5D=cod&credit_card%5Bcnb%5D=4033920041674989&credit_card%5Bmonth%5D=11&credit_card%5Byear%5D=2022&credit_card%5Bvval%5D=909&order%5Bterms%5D=0&order%5Bterms%5D=1&hpcvv=&commit=%E8%B3%BC%E5%85%A5%E3%81%99%E3%82%8B"
has_cookie = False
file_name = "cookie"
stock = "http://www.supremenewyork.com/mobile_stock.json?_="
property = "http://www.supremenewyork.com/shop/"
info = "http://1.surpreme.applinzi.com/" + index
goods_info = {}
ids = {}
upload_url = "http://surphp.applinzi.com/upload.php"


# ssl._create_default_https_context = ssl._create_unverified_context

class shop(object):
    def __init__(self):
        self.cj = cookiejar.MozillaCookieJar(file_name)
        if (has_cookie):
            self.cj.load(file_name, ignore_discard=True, ignore_expires=True)
        self.handler = HTTPCookieProcessor(self.cj)
        self.opener = build_opener(self.handler)

    def getInfo(self):
        print("Start")
        url = info
        req = Request(url, method="GET")
        response = self.opener.open(req)
        response = response.read().decode('utf-8')
        return response

    def browaer(self, url):
        # post_data = urllib.urlencode(post)
        req = Request(url)
        response = self.opener.open(req)

        for item in self.cj:
            print('Name = ' + item.name)
            print('Value = ' + item.value)
        self.cj.save(ignore_discard=True, ignore_expires=True)
        has_cookie = True
        return True

    def getGoods(self):
        self.starttime = time.time()
        url = stock + str(int(time.time()))
        req = Request(url, method="GET")
        req.add_header("User-Agent",
                       "Mozilla/5.0 (iPhone; CPU iPhone OS 10_2 like Mac OS X) AppleWebKit/602.3.12 (KHTML, like Gecko) Mobile/14C92 MicroMessenger/6.5.9 NetType/WIFI Language/zh_CN")
        response = self.opener.open(req)
        response = response.read().decode('utf-8')
        print(str(time.time() - self.starttime) + "s cost")
        j = json.loads(response)['products_and_categories']
        for k in goods_info:  # 所有的想抢的货的信息
            catAll = j[k]  # 每个种类的货的信息
            for g in catAll:  # 每个货
                for h in goods_info[k]:  # 每个要匹配的名字
                    if h in g['name']:
                        print(g['name'])
                        property = cls_shop.getProperty(g['id'])
                        data = cls_shop.getProData(property)
                        if (data != None):
                            return cls_shop.add_good(g['id'], data)
                        else:
                            print("no stock")
                            print()
                            print()

        return False

    def getProData(self, data):
        for pro in data:
            size = pro['sizes']
            for i in size:
                if i['stock_level'] == 1:
                    postDict = {
                        'utf8': '✓',
                        'style': pro['id'],
                        'size': i['id'],
                        'commit': 'カートに入れる'
                    }
                    return urlencode(postDict)
        return None

    def getProperty(self, id):
        url = property + str(id) + ".json"
        req = Request(url, method="GET")
        response = self.opener.open(req)
        response = response.read().decode('utf-8')
        j = json.loads(response)['styles']
        return j
        # for i in j:
        #     print(i)
        # j = json.loads(response)['products_and_categories']
        # for i in j:
        #     print(i)
        #     for k in j[i]:
        #         name = k['name']
        #         if 'The North Face' in name and 'Tee' in name:
        #             print(k)

    def add_good(self, id, post):
        # post_data = urllib.urlencode(post)
        url = goodsurl + str(id) + "/add"
        print(url)
        print(post)
        req = Request(url, post.encode(encoding='UTF8'))
        response = self.opener.open(req)
        # for item in self.cj:
        #     print('Name = ' + item.name)
        #     print('Value = ' + item.value)
        self.cj.save(ignore_discard=True, ignore_expires=True)
        has_cookie = True
        print("success")
        print(str(time.time() - self.starttime) + "s cost")
        print()
        return True
        # print response.read()

    def pre_checkout(self, url):
        # post_data = urllib.urlencode(post)
        req = Request(url)
        response = self.opener.open(req)
        self.cj.save(ignore_discard=True, ignore_expires=True)
        has_cookie = True
        for item in self.cj:
            print('Name = ' + item.name)
            print('Value = ' + item.value)
        print("")
        res = response.read().decode('utf-8')
        print(str(time.time() - self.starttime) + "s cost")
        print("end")
        return quote(re.findall(r'<meta name="csrf-token" content="(.+?)"', res)[0])  #

    def checkout(self, url, post):
        # post_data = urllib.urlencode(post)
        ck = cookiejar.Cookie(version=0, name='lastid', value='1513704371715', port=None, port_specified=False,
                              domain='www.abc.cn', domain_specified=False, domain_initial_dot=False, path='/',
                              path_specified=True, secure=False, expires=None, discard=True, comment=None,
                              comment_url=None, rest={'HttpOnly': None}, rfc2109=False)
        self.cj.set_cookie(ck)
        req = Request(url, post.encode(encoding='UTF8'))
        response = self.opener.open(req)
        self.cj.save(ignore_discard=True, ignore_expires=True)
        has_cookie = True
        for item in self.cj:
            print('Name = ' + item.name)
            print('Value = ' + item.value)
        print("")
        res = response.read().decode('utf-8')
        print(res)
        file.write(res)

        print(str(time.time() - self.starttime) + "s cost")
        print("end")

    def upload(self, url, files):
        r = requests.post(url, files=files)


def alive():
    delta = datetime.datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S') - datetime.datetime.now()
    print('I am alive, left %s' % delta)
    print('now is %s' % datetime.datetime.now())
    print(goods_info)
    print()


def start_bot():
    if cls_shop.getGoods():
        # cls_shop.browaer()
        # token = cls_shop.pre_checkout(checkout_url)
        # pattern = 'authenticity_token=(.*?)&'
        # check_auth_post = re.sub(pattern, "authenticity_token=" + token + "&", check_post)
        # print(check_auth_post)
        cls_shop.checkout(checkout_json__url, check_post)
        bot.remove()
        thread.shutdown(wait=False)
        file.close()
        files = {'myFile': (
            index + "__" + datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + ".txt",
            open(upload_file_name, 'r+'))}
        cls_shop.upload(upload_url, files=files)
        # else:
        #     bot.remove()
        #     thread.shutdown(wait=False)


if __name__ == '__main__':
    index = "4"
    info = "http://1.surpreme.applinzi.com/" + index
    print(index)
    cls_shop = shop()
    response = cls_shop.getInfo()
    # response = '{"commit":"utf8=%E2%9C%93&authenticity_token=CHcaHKo5H2t238nknlp2%2B%2Bi%2F7WcYQ3JqZmr%2BNrsdI7XDMfWJMvfZ1P1Lp0GLIi%2F4aIbJA97TmENIkKn8Gvu8hA%3D%3D&credit_card%5Blast_name%5D=wang&credit_card%5Bfirst_name%5D=jiarui&order%5Bemail%5D=1198222311%40qq.com&order%5Btel%5D=09098229503&order%5Bbilling_state%5D=+%E6%9D%B1%E4%BA%AC%E9%83%BD&order%5Bbilling_city%5D=%E6%9D%B1%E4%BA%AC%E9%83%BD&order%5Bbilling_address%5D=%E6%9D%B1%E4%BA%AC%E9%83%BD%E6%96%B0%E5%AE%BF%E5%8C%BA%E4%B8%8A%E8%90%BD%E5%90%881-15-12Imagin%E4%B8%8B%E8%90%BD%E5%90%881-a&order%5Bbilling_zip%5D=161-0034&same_as_billing_address=1&credit_card%5Btype%5D=cod&credit_card%5Bcnb%5D=aq&credit_card%5Bmonth%5D=12&credit_card%5Byear%5D=2024&credit_card%5Bvval%5D=a&order%5Bterms%5D=0&order%5Bterms%5D=1&hpcvv=","isValid":1,"time":"2017-12-16 10:59:45","goods":[{"category":"Accessories","name":["Crew Socks"]}]}'
    j = json.loads(response)
    print(j)
    upload_file_name = index + ".txt"
    file = open(upload_file_name, 'w')
    print(j)
    if (j['isValid'] != 1):
        sys.exit()
    goods = j['goods']
    check_post = str(j['commit'])
    print(check_post)
    starttime = j['time']
    # starttime = '2017-12-14 23:46:00'
    for cat in goods:
        goods_info[cat['category']] = cat['name']

    thread = BlockingScheduler()
    alivetrigger = CronTrigger(second='*/5',
                               end_date=datetime.datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S') - datetime.timedelta(
                                   seconds=6))
    alive = thread.add_job(alive, alivetrigger)
    bottrigger = CronTrigger(start_date=datetime.datetime.strptime(starttime, '%Y-%m-%d %H:%M:%S'))
    bot = thread.add_job(start_bot, bottrigger)
    thread.start()
