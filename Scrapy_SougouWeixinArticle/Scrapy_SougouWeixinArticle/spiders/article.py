# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlencode
from scrapy import Request
from ..items import SogouWeixinArticleItem,WeixinArticleItemloader
import datetime
from utlis.common import get_md5

class ArticleSpider(scrapy.Spider):
    name = 'article'
    allowed_domains = ['weixin.sogou.com/weixin?']
    start_urls = ['http://weixin.sogou.com/weixin?/']

    custom_settings = {
        "COOKIES_ENABLED":False,
        # "DOWNLOAD_DELAY": 2,
        "DEFAULT_REQUEST_HEADERS":{
            "Connection":" keep-alive",
            "Cookie":"IPLOC=CN3201; SUID=A1BC41DF2320940A000000005ADAE3FE; SUV=1524294655452323; ABTEST=5|1524294660|v1; SNUID=F3EE138C53563805D2955B9853D01DFE; weixinIndexVisited=1; JSESSIONID=aaa-T5zYnpHzDc6eYwViw; sct=2; ppinf=5|1524296019|1525505619|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozOTolNDAlRTQlQjglOTElRTUlODUlQUIlRTYlODAlQUElRUYlQkMlOEF8Y3J0OjEwOjE1MjQyOTYwMTl8cmVmbmljazozOTolNDAlRTQlQjglOTElRTUlODUlQUIlRTYlODAlQUElRUYlQkMlOEF8dXNlcmlkOjQ0Om85dDJsdUNyLWFQOTRCRlZKck9seVkzcTVDaklAd2VpeGluLnNvaHUuY29tfA; pprdig=t0Syg-1-CUcmAxzznu-WZ5hXKclN87Q432EixoMeBXJfbedm6jhFCWGlKLULvFHbhwunvzYZ-TptQ6SpFu6xzvYkB0NIEmzGaa-OSFbjbdl8rP5IdlgluYgSwA0VTboeFqVdjpXyzxboILuK0YBcU-nFDFkCdywZB0u0UUNrZNA; sgid=08-34120369-AVra6VPP9Cz4XUPTDlwKFyU",
            "Host":"weixin.sogou.com",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36"
                }
            }

    def start_requests(self):
        data = {
            "type":"2",
            "s_from":"input",
            "query":"人工智能",
            "ie":"utf8",
            }
        query_data = urlencode(data)
        url = "http://weixin.sogou.com/weixin?"+query_data
        yield Request(url=url,callback=self.parse,dont_filter=True)


    def parse(self,response):
        headers = {
            "Host":"mp.weixin.qq.com",
            # "Cookie":"IPLOC=CN3201; SUID=A1BC41DF2320940A000000005ADAE3FE; SUV=1524294655452323; ABTEST=5|1524294660|v1; SNUID=F3EE138C53563805D2955B9853D01DFE; weixinIndexVisited=1; JSESSIONID=aaa-T5zYnpHzDc6eYwViw; sct=2; ppinf=5|1524296019|1525505619|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozOTolNDAlRTQlQjglOTElRTUlODUlQUIlRTYlODAlQUElRUYlQkMlOEF8Y3J0OjEwOjE1MjQyOTYwMTl8cmVmbmljazozOTolNDAlRTQlQjglOTElRTUlODUlQUIlRTYlODAlQUElRUYlQkMlOEF8dXNlcmlkOjQ0Om85dDJsdUNyLWFQOTRCRlZKck9seVkzcTVDaklAd2VpeGluLnNvaHUuY29tfA; pprdig=t0Syg-1-CUcmAxzznu-WZ5hXKclN87Q432EixoMeBXJfbedm6jhFCWGlKLULvFHbhwunvzYZ-TptQ6SpFu6xzvYkB0NIEmzGaa-OSFbjbdl8rP5IdlgluYgSwA0VTboeFqVdjpXyzxboILuK0YBcU-nFDFkCdywZB0u0UUNrZNA; sgid=08-34120369-AVra6VPP9Cz4XUPTDlwKFyU",
            "User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.117 Safari/537.36"
            }
        selector = response.css("ul.news-list li")

        for sel in selector:
            article_urls = sel.css(".txt-box h3 a::attr(href)").extract()
            for article_url in article_urls:
                article_url = article_url.replace("*","%2A")
                yield Request(url=article_url,callback=self.parse_article,headers=headers,dont_filter=True)

        #获取下一页的url
        next_url = response.css("a#sogou_next::attr(href)").extract_first()
        print(next_url)
        if next_url:
            url = response.urljoin(next_url)
            yield Request(url=url,callback=self.parse,dont_filter=True)


    def parse_article(self,response):
        # title = response.css("h2#activity-name::text").extract_first()
        # time = response.css("#post-date::text").extract_first()
        # author = response.css("#post-user::text").extract_first()
        # content = response.css("div#js_content p").extract()
        # print(response.text)
        #通过Itemloader获取具体的信息
        url_object_id = get_md5(response.url)
        item_loader = WeixinArticleItemloader(item=SogouWeixinArticleItem(),response=response)
        item_loader.add_value("url",response.url)
        item_loader.add_value("url_object_id",url_object_id)
        item_loader.add_css("title","h2#activity-name::text")
        item_loader.add_css("time","#post-date::text")
        item_loader.add_css("author","#post-user::text")
        item_loader.add_css("content","div#js_content")
        item_loader.add_value("crawl_time",datetime.datetime.now())
        article = item_loader.load_item()
        yield article

