#scraper for scraping the vizer database
# (for more info email kriekvdmeulen@gmail.com)

import scrapy
import json
import time
from scrapy.crawler import CrawlerProcess
class QuotesSpider(scrapy.Spider):
    name = "viezier"

    def start_requests(self):

        jsonFile = open("fluxvar.json",'r')
        datalist = json.load(jsonFile)

# read in initial page from json
        for entry in datalist:

            yield scrapy.Request(url=entry['url'], callback=self.next,\
            meta={'id':entry['id']})

# go to next page
    def next(self,response):
        yield scrapy.http.FormRequest.from_response(response,callback=self.parse,\
        meta={'id':response.meta['id']})

# fetch the actual data from vizer
    def parse(self, response):

        rows = response.css("table.sort tr")[1:]
        if rows:
            for row in rows:
                data = row.css('td::text').extract()[4:7]
                nu = data[0]
                s_nu = data[1]
                e = data[2]


                yield {
                    'nu': nu,
                    's_nu': s_nu,
                    'e': e,
                    'id':response.meta['id']
                }
        else:
            yield {
                'nu': [],
                's_nu': [],
                'e': [],
                'id':response.meta['id']
            }

# process = CrawlerProcess({
#     'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
# })
#
# d = process.crawl(QuotesSpider)
# process.start()
