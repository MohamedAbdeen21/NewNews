# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from itemloaders.processors import TakeFirst, MapCompose, Compose, Join
import re

words_to_delete = [
    'Advertisment',
    'Supported by',
    'To revist this article, visit My Profile, then']
def clean_text(text):
    if any(word == text for word in words_to_delete): return ''
    return re.sub("[ |\|]{2,}","",text.replace('\n','').replace('\t','').replace('\r','').replace(',','').replace('"','').replace('&quot;','').replace(';',''))

class XmlscraperItem(scrapy.Item):
    url = scrapy.Field(output_processor = TakeFirst())
    text = scrapy.Field(input_processor = MapCompose(clean_text), output_processor = Join())
    title = scrapy.Field(input_processor = MapCompose(clean_text), output_processor = TakeFirst())
    count = scrapy.Field(input_processor = MapCompose(clean_text,str.split), output_processor = Compose(len))
    date = scrapy.Field(output_processor = TakeFirst())
    pass
