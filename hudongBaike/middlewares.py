# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

import logging
import random
#from hudongBaike.util import Util
from scrapy.exceptions import IgnoreRequest


class RandomUserAgent(object):
    def __init__(self, agents):
        self.agents = agents

    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))

    def process_request(self, request, spider):
        request.headers.setdefault('User-Agent', random.choice(self.agents))



class ProxyMiddleware(object):
    def __init__(self):
        self.failed_proxies = set()
        #self.proxies = Util.get_proxy_list(500)
        self.ttl = 3000


    def process_request(self, request, spider):
        #if self.ttl > 0:
        #    self.ttl = self.ttl - 1
        #else:
        #    self.proxies = self.proxies + [
        #        i for i in Util.get_proxy_list(500)
        #        if i not in self.failed_proxies]
        #    logging.info("Add a batch of proxies, Total: {0}".format(len(self.proxies)))
        #    self.ttl = 3000
        #proxy = random.choice(self.proxies)
        proxy = "218.76.253.201:61310"  # 测试ip是否会封?
        request.meta['proxy'] = "http://{0}".format(proxy)

    
    def process_exception(self, request, exception, spider):
        #proxy = request.meta['proxy']
        #logging.info('Removing failed proxy {0}'.format(proxy))
        #try:
        #    self.proxies.remove(proxy)
        #   self.failed_proxies.add(proxy)
        #except ValueError:
        #    pass
        logging.info("Error in ProxyMiddleware process_exception() !")
    

    def process_response(self, request, response, spider):
        if response.status in [400, 403, 404, 407, 408, 429, 500, 501, 502, 503, 504]:
            raise IgnoreRequest
        else:
            return response
