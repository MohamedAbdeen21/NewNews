import scrapy
from xmlscraper.rssfeeds import websiteLinks
import xmlscraper.properties as properties

from datetime import datetime
from dateutil import parser as timeparser

from scrapy.utils.project import get_project_settings
from scrapy.crawler import CrawlerProcess
from scrapy.loader import ItemLoader
from scrapy.http import TextResponse

from xmlscraper.xmlscraper.items import XmlscraperItem

import requests
import feedparser
import logging


logging.basicConfig(filename='scraper.log')

class XmlscrapeSpider(scrapy.Spider):
    name = 'xmlscrape'
    def __init__(self):
        self.timeout_time = 20
        self.start_urls = websiteLinks
        self.count = 0
        self.today = properties.today
        self.unique_urls = []
        

    def parse(self, response):
        feed = feedparser.parse(response.url)
        try:
            for entry in feed['entries']:
                time = datetime.date(timeparser.parse(entry['published']))
                uniqueness_flag = entry['link'] not in self.unique_urls

                if time == self.today and uniqueness_flag:
                    self.unique_urls.append(entry['link'])
                    self.count += 1
                    # Get the HTML to get the text, instead of using the entry['summary']
                    textResponse = requests.get(entry['link'], timeout = self.timeout_time, headers = {"User-Agent":properties.USER_AGENT})
                    textResponse = TextResponse(body = textResponse.content, url=entry['link'])

                    # Load the item
                    loader = ItemLoader(item = XmlscraperItem(), selector=textResponse)
                    loader.add_value('url', entry['link'])
                    loader.add_value('title', entry['title'])
                    loader.add_css('text', "body p::text")
                    loader.add_value('date',time)
                    loader.add_css('count', "body p::text" )
                    if 'tags' in entry.keys():
                        loader.add_value('tags', [tag.get('term') for tag in entry['tags']])
                    else:
                        loader.add_value('tags', ['NULL'])

                    print(f"Article\t{self.count}: {entry['link']}")
                    yield loader.load_item()
                elif not uniqueness_flag:
                    print("Discarded a duplicate!")
        except KeyError as exception:
            print("Can't access parsed data due to {} in url {}".format(repr(exception),response.url))
            yield None
        except requests.exceptions.Timeout as exception:
            print('URL {} took too long to respond (more than {} seconds).'.format(entry['link'],self.timeout_time))
            yield None


def run():
    settings = get_project_settings()
    # settings.update({"FEEDS":{"sample2.csv":{
    #     "format":"csv",
    #     "encoding": "utf-8",
    #     "overwrite": True,
    #     "fields": ["url","title","text","count","date"],
    #     }}})
    process = CrawlerProcess(settings)

    logging.getLogger('scrapy').propagate = False
    logging.getLogger('protego').propagate = False
    logging.getLogger('urllib3').propagate = False

    process.crawl(XmlscrapeSpider)
    process.start()