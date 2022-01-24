from dataclasses import dataclass
import scrapy
import json5
LINKS_SELECTOR = "a::attr(href)"
STANDARD_LINK = "https://www.hydrocarbonprocessing.com/"
result = []

@dataclass
class NewsItem(object):
    title: str
    url: str
    date: str
    content: str

# def create_url():
#     res = scrapy.Request.parse(url='https://www.hydrocarbonprocessing.com/news?page=1')
#
#     response = res
#     print("******************************")
#     print(response)
#     print("******************************")
#     urls = []
#     return urls

def create_urls():
    urls = []
    for page_number in range(1, 1):
        urls.append(f'https://www.hydrocarbonprocessing.com/news?page={page_number}')
    return urls

class Content(scrapy.Spider):
    name = "content"

    def start_requests(self):
        urls = ['/news/2021/11/arbor-renewable-gas-announces-plant-site-locations', '/news/2021/11/australia-promotes-biofuels-growth-to-help-fight-climate-change']
        for url in urls:
            yield scrapy.Request(url=STANDARD_LINK + url, callback=self.parse)

    def parse(self, response):
        data = response.css("div.article-content")
        for link in data:
            result.append({"Title": link.css('h1.article-title::text').extract_first(),
                           "Date": link.css('div.date-line::text').extract_first(),
                           "Content": link.css('p::text').extract()})


        # save to json file
        with open('data.json', 'w') as f:
            json5.dump(result, f, indent=2, encoding='utf-8')
