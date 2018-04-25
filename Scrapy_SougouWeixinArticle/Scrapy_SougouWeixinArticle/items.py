# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from scrapy.loader.processors import TakeFirst,MapCompose,Join
from w3lib.html import remove_tags
from settings import SQL_DATETIME_FORMAT


class ScrapySougouweixinarticleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class WeixinArticleItemloader(ItemLoader):
    default_output_processor = TakeFirst()


def remove_blank(value):
    return value.strip()

def return_value(value):
    return value

class SogouWeixinArticleItem(scrapy.Item):
    url = scrapy.Field()
    url_object_id = scrapy.Field()
    title = scrapy.Field(input_processor=MapCompose(remove_blank))
    time = scrapy.Field()
    author = scrapy.Field()
    content = scrapy.Field(input_processor=MapCompose(remove_tags,return_value,remove_blank))
    crawl_time = scrapy.Field()


    def get_insert_sql(self):
        insert_sql = """
            insert into WeixinArticle (url,url_object_id,title,time,author,content,crawl_time) VALUES (%s,%s,%s,%s,%s,%s,%s) 
        """
        params = (
            self["url"], self["url_object_id"], self["title"], self["time"], self["author"], self["content"],
            self["crawl_time"].strftime(SQL_DATETIME_FORMAT)
        )

        return insert_sql, params