#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import urllib
import urllib2
import cookielib

goods1 = 'http://www.supremenewyork.com/shop/accessories/etciwvr9l'
cart = 'http://www.supremenewyork.com/shop/cart'
post_data = {}


class shop(object):
    def __init__(self):
        self.cj = cookielib.CookieJar()
        self.handler = urllib2.HTTPCookieProcessor(self.cj)
        self.opener = urllib2.build_opener(self.handler)

    def add_good(self, url, post):
        post_data = urllib.urlencode(post)
        req = urllib2.Request(url)
        response = self.opener.open(req)
        print response.read()


if __name__ == '__main__':
    cls_shop = shop()
    cls_shop.add_good(goods1, post_data)
