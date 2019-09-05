import logging
import scrapy
import codecs
import urllib.parse
import re
import os
import time
from bs4 import BeautifulSoup
#from hudongBaike.util import Util
from hudongBaike.items import HudongbaikeItem


class MySpider(scrapy.spiders.CrawlSpider):
    name = "hudongBaike"
    #util = Util()
    allowed_domains = [
        "www.baike.com",
        "baike.com",
        "www.hudong.com",
    ]
    start_urls = [
        "http://fenlei.baike.com/",
    ]
    

    def parse(self, response):
        soup = BeautifulSoup(response.body, "lxml")
        links = soup.find_all("a")
        arr = []
        for l in links:
            try:
                href = l["href"]
                arr.append(href)
            except:
                pass
        for a in arr:
            pattern = "".join([
                "http://www\.baike\.com.*|",
                "http://fenlei\.baike\.com.*|",
                "http://weibaike\.baike\.com.*|",
                "http://www\.hudong\.com.*",
            ])
            if re.match(pattern, a):
                yield scrapy.http.request.Request(a, callback=self.parse)

        url = urllib.parse.unquote(response.url).strip()  # 去除空字符
        rst = re.match("http://www.baike.com/wiki/.*", url)
        if rst:
            content = soup.find("div", attrs = {"class": "w-990"})
            h1 = soup.find("h1")
            if content is None or h1 is None:  # 数据丢失
                #logging.info("Content is None: " + url)
                yield scrapy.http.request.Request(response.url, callback = self.parse)
                return

            filename = re.sub("[/?&=#.\"'\\:*<>\|]", "_", url.split("/", 4)[-1])
            pre = "F://" + '-'.join([str(i) for i in time.localtime()[:3]]) + "/"
            try:
                os.makedirs(pre)
            except:
                pass
            savePath = pre + filename
            with codecs.open(savePath, 'wb', encoding = "utf-8-sig") as f:
                f.write(str(content))

            title = h1.get_text().strip()
            prefix = re.sub("\[.*\]", "", title)
            # 写入数据库记录
            item = HudongbaikeItem()
            item['URL'] = url
            item['Place'] = savePath
            item['Title'] = title
            item['Prefix'] = prefix
            yield item