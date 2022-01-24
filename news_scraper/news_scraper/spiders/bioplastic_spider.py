import scrapy
from scrapy.crawler import CrawlerRunner
from crochet import setup, wait_for
setup()
result = []
urls = []
STANDARD_LINK = "https://www.sustainableplastics.com"


class PlasticLinks(scrapy.Spider):
    name = "Links"
    start_urls = [f'https://www.sustainableplastics.com/bioplastics?page={page}' for page in range(0, 5)]
    custom_settings = {
        'FEEDS': {
            'news.csv': {
                'format': 'csv',
                'overwrite': True
            }
        }
    }

    def parse(self, response):
        apts = response.css("div.view-content div.views-row a::attr(href)").getall()
        for apt in apts:
            url = STANDARD_LINK + apt
            if url in urls:
                continue
            else:
                urls.append(url)


class PlasticArticles(scrapy.Spider):
    name = "Articles"
    start_urls = urls
    custom_settings = {
        'FEEDS': {
            'news.csv': {
                'format': 'csv',
                'overwrite': True
            }
        }
    }

    def parse(self, response):
        element = response.css("div.block-region-content-left")
        result.append(
            {"Date": element.css('span.text-gray::text').extract_first(),
             "Title": element.css('div.content h1::text').extract_first(),
             "Content": element.css("p::text").extract()})


@wait_for(10)
def scrap_links():
    crawler = CrawlerRunner()
    d = crawler.crawl(PlasticLinks)
    return d


@wait_for(60)
def scrap_articles():
    crawler = CrawlerRunner()
    d = crawler.crawl(PlasticArticles)
    return d

scrap_links()
scrap_articles()