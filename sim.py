#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import urllib
import urllib2
import cookielib

baidu = "http://www.baidu.com";
goods1 = 'http://www.supremenewyork.com/shop/4631/add'
post_data1 = "utf8=%E2%9C%93&style=17485&size=48018&commit=%E3%82%AB%E3%83%BC%E3%83%88%E3%81%AB%E5%85%A5%E3%82%8C%E3%82%8B"
cart = 'http://www.supremenewyork.com/shop/cart'


class shop(object):
    def __init__(self):
        self.cj = cookielib.CookieJar()
        self.handler = urllib2.HTTPCookieProcessor(self.cj)
        self.opener = urllib2.build_opener(self.handler)

    def add_good(self, url, post):
        # post_data = urllib.urlencode(post)
        req = urllib2.Request(url, post)
        response = self.opener.open(req)
        for item in self.cj:
            print 'Name = ' + item.name
            print 'Value = ' + item.value
            # print response.read()


if __name__ == '__main__':
    cls_shop = shop()
    cls_shop.add_good(goods1, post_data1)
