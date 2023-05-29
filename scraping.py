import scrapy
import w3lib.html
import sys
import os.path
from scrapy.crawler import CrawlerProcess
from scrapy.crawler import CrawlerRunner
from scrapy.selector import Selector
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from twisted.internet import reactor, defer
from utils import Utils

urls = []  # Represents the list of urls that we will webscrap

# definition of a first scrapy spider used to retrieve the content of each url and save it to a local file
class GriffithArticleFetchSpider(scrapy.Spider):
    name = "griffith_articles_fetch"
    allowed_domains = ["https://www.griffith.ie", "www.griffith.ie"]
    start_urls = urls
    counter = 1

    def parse(self, response):
        result = " ".join(response.css(".basic-page__content").getall())

        result = w3lib.html.replace_tags(text=result, token=" ")
        result = w3lib.html.replace_escape_chars(text=result, replace_by=" ")
        if len(result) < 20:
            return

        filename = "D" + str(self.counter)
        of = open(sys.argv[1] + "/" + filename, "w")
        of.write(result)
        of.close()

        relations_file = open("relationship_url_document.csv", "a")
        relations_file.write(filename + ", " + response.url + "\n")
        relations_file.close()

        self.counter += 1


# Definition of a second scrapy spider used to browse the initial url and get the first 20 urls of the page
class GriffithGoodLinkSpider(scrapy.Spider):
    name = "griffith_top_20_links"
    allowed_domains = ["https://www.griffith.ie", "www.griffith.ie"]
    start_urls = [
        "https://www.griffith.ie",
    ]

    visited = {}  # Represents the list of urls already visited
    cnt = 40

    def parse(self, response):
        global urls
        for link in response.xpath("//a/@href").getall():
            if self.cnt == 0:
                break
            if (
                not self.visited.get(str(link))
                and link.startswith("/")
                and not link.startswith("/cdn-cgi")
            ):
                self.visited[str(link)] = True
                self.cnt -= 1
                url = "https://www.griffith.ie" + str(link)
                urls.append(url)

# Run the spiders asynchronously
@defer.inlineCallbacks
def crawl(runner):
    yield runner.crawl(GriffithGoodLinkSpider)
    yield runner.crawl(GriffithArticleFetchSpider)

    reactor.stop()


def main():
    open("relationship_url_document.csv", "w").close()

    dirname = Utils().parse_args(1, "python scrapping.py <outfolder>")
    Utils().create_dir(dirname)

    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)

    crawl(runner)
    reactor.run()


if __name__ == "__main__":
    main()
