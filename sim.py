#!/usr/bin/env python
# _*_ coding:utf-8 _*_

import ssl
import urllib2
import cookielib

baidu = "http://www.baidu.com";
goods1 = 'http://www.supremenewyork.com/shop/4631/add'
goods2 = 'http://www.supremenewyork.com/shop/4632/add'
post_data1 = "utf8=%E2%9C%93&style=17485&size=48018&commit=%E3%82%AB%E3%83%BC%E3%83%88%E3%81%AB%E5%85%A5%E3%82%8C%E3%82%8B"
post_data2 = "utf8=%E2%9C%93&style=17486&size=48019&commit=%E3%82%AB%E3%83%BC%E3%83%88%E3%81%AB%E5%85%A5%E3%82%8C%E3%82%8B"
cart = 'http://www.supremenewyork.com/shop/cart'
checkout = 'http://www.supremenewyork.com/checkout'
check_post="utf8=%E2%9C%93&authenticity_token=mPkjLpIb8Y7n%2FN5jTVv7kEy2isS2Etv8gcKJOk5mFjv5%2FWCvEmwT6a%2FabUQSnFZHB0ASfJUbVlif8Rw87R%2Fv8Q%3D%3D&credit_card%5Blast_name%5D=cheng&credit_card%5Bfirst_name%5D=hao&order%5Bemail%5D=123123&order%5Btel%5D=1231&order%5Bbilling_state%5D=+%E5%AE%AE%E5%9F%8E%E7%9C%8C&order%5Bbilling_city%5D=123&order%5Bbilling_address%5D=123&order%5Bbilling_zip%5D=123&same_as_billing_address=1&store_address=1&credit_card%5Btype%5D=visa&credit_card%5Bcnb%5D=1231+2332+13__+____&credit_card%5Bmonth%5D=11&credit_card%5Byear%5D=2017&credit_card%5Bvval%5D=1111&order%5Bterms%5D=0&order%5Bterms%5D=1&hpcvv=&commit=%E8%B3%BC%E5%85%A5%E3%81%99%E3%82%8B"
has_cookie = False
file_name = "cookie"

ssl._create_default_https_context = ssl._create_unverified_context

class shop(object):
    def __init__(self):
        self.cj = cookielib.MozillaCookieJar(file_name)
        if (has_cookie):
            self.cj.load(file_name, ignore_discard=True, ignore_expires=True)
        self.handler = urllib2.HTTPCookieProcessor(self.cj)
        self.opener = urllib2.build_opener(self.handler)

    def add_good(self, url, post):
        # post_data = urllib.urlencode(post)
        req = urllib2.Request(url, post)
        response = self.opener.open(req)
        for item in self.cj:
            print 'Name = ' + item.name
            print 'Value = ' + item.value
        print ""
        self.cj.save(ignore_discard=True, ignore_expires=True)
        has_cookie = True
        # print response.read()

    def checkout(self, url, post):
        # post_data = urllib.urlencode(post)
        req = urllib2.Request(url, post)
        response = self.opener.open(req)
        self.cj.save(ignore_discard=True, ignore_expires=True)
        has_cookie = True
        print response.read()


if __name__ == '__main__':
    cls_shop = shop()
    cls_shop.add_good(goods1, post_data1)
    cls_shop.add_good(goods2, post_data2)
    cls_shop.checkout(checkout, check_post)
