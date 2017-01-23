# -*- coding: utf-8 -*-
import scrapy
import re
from scrapy import Selector

from seekjob.items import SeekjobItem

import urllib
import codecs
import sys
reload(sys)

keyword = "数据分析"
keywordcode = urllib.quote(keyword)

is_start_page = True                            # whether the start page

class Job51Spider(scrapy.Spider):
    name = "job51"
    allowed_domains = ["51job.com"]
    start_urls = [
        "http://search.51job.com/jobsearch/search_result.php?fromJs=1&keyword=" + keywordcode,
                 ]

    def parse(self, response):                 #find the start url
        global is_start_page

        if is_start_page:                      # if now is the start page
            url = self.start_urls[0]
            is_start_page = False              # prepare for next page
        else:                                  # if not, return the link of "nextpage"
            href = response.xpath("*//li[@class='bk']/a/@href")             # get "nextpage" url
            url = response.urljoin(href.extract())

        yield scrapy.Request(url, callback=self.parse_dir_url)

    def parse_dir_url(self, response):                                           # catch the inner url
        for sel in response.xpath("//*[@id='resultList']/div/p/span/a/@href"):
            full_url = response.urljoin(sel.extract())
            yield scrapy.Request(full_url, callback=self.parse_dir_item)

        next_page = response.xpath("*//li[@class='bk']/a/@href")                 # control rolling-page
        if next_page:
            url = response.urljoin(next_page[0].extract())                      # there are two 'bk' node in A source
            print "!!!!!!!!!!!markherehhhh" + url
            yield scrapy.Request(url, callback=self.parse_dir_url)

    def parse_dir_item(self, response):

        #remove empty list element
        tempjobdc = []
        for i in response.xpath("*//div[@class='tBorderTop_box'][1]/div[1]/text()").extract():
            if re.search(r'[\u4e00-\u9fa5_a-zA-Z0-9]',i) != None:
                tempjobdc.append(i)
        jobdccontent = "".join(tempjobdc)                                                      # turn list to string
        content = re.sub("' '+|\t+|\n+|\s+|\r+", "", jobdccontent)                             # get rid of space & tab
        #---------------------------

        item = SeekjobItem()
        item['title'] = response.xpath("*//div[@class='cn']/h1/@title").extract()[0]
        item['link'] = response.url.encode('utf-8')
        item['salary'] = response.xpath("*//div[@class='cn']/strong/text()").extract()
        item['jobdc'] = content


        yield item





