import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.selector import Selector

visited = {}
cnt = 20

class GriffithSpider(scrapy.Spider):
    name = "griffith_top_20_articles"
    allowed_domains = ['https://www.griffith.ie', 'www.griffith.ie']
    start_urls = [
        "https://www.griffith.ie",
    ]

    def parse(self, response):
        global cnt
        for link in response.xpath("//a/@href").getall():
            if cnt == 0:
                break
            if not visited.get(str(link)) and link.startswith("/") and not link.startswith("/cdn-cgi"):
                link.x
                visited[str(link)] = True
                cnt -= 1
                print(str(link))

process = CrawlerProcess(
    {
        "USER_AGENT": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/111.0"
    }
)



process.crawl(GriffithSpider)
process.start()
