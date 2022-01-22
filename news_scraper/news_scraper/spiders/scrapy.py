import scrapy


class Titles(scrapy.Spider):
    name = "titles"

    def start_requests(self):
        urls = [
            'https://www.hydrocarbonprocessing.com/news?page=1'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        filename = f'test.html'
        with open(filename, 'wb') as f:
            f.write(response.body)

