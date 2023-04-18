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

urls = []  # Represents the list of urls that we will webscrap
visited = {}  # Represents the list of urls already visited
cnt = 40
counter = 1


# definition of a first scrapy spider used to retrieve the content of each url and save it to a local file
class GriffithArticleFetchSpider(scrapy.Spider):
    name = "griffith_articles_fetch"
    allowed_domains = ["https://www.griffith.ie", "www.griffith.ie"]
    start_urls = urls

    def parse(self, response):
        global counter
        result = str(
            w3lib.html.replace_tags(
                str(response.css(".basic-page__content").getall()), "  "
            )
        )
        if len(result) < 20:
            return

        filename = "D" + str(counter)
        of = open(sys.argv[1] + "/" + filename, "w")
        of.write(result)
        of.close()

        relations_file = open(sys.argv[1] + "/" + "relations.csv", "a")
        relations_file.write(filename + ", " + response.url + "\n")
        relations_file.close()

        counter += 1


# Definition of a second scrapy spider used to browse the initial url and get the first 20 urls of the page
class GriffithGoodLinkSpider(scrapy.Spider):
    name = "griffith_top_20_links"
    allowed_domains = ["https://www.griffith.ie", "www.griffith.ie"]
    start_urls = [
        "https://www.griffith.ie",
    ]

    def parse(self, response):
        global urls
        global cnt
        for link in response.xpath("//a/@href").getall():
            if cnt == 0:
                break
            if (
                not visited.get(str(link))
                and link.startswith("/")
                and not link.startswith("/cdn-cgi")
            ):
                visited[str(link)] = True
                cnt -= 1
                url = "https://www.griffith.ie" + str(link)
                urls.append(url)


# Create a new folder for saving the fetched files and check whether the folder already exists. If the folder exists, the script will exit
def cleanup_and_create_folder(dirname):
    if os.path.exists(dirname):
        print("folder you specified already exists! Please remove it first")
        sys.exit()

    os.makedirs(dirname)


if len(sys.argv) != 2:
    print("Please insert directory paths: python scrapping.py <outfolder>")
    sys.exit()

cleanup_and_create_folder(sys.argv[1])
settings = get_project_settings()
configure_logging(settings)
runner = CrawlerRunner(settings)


# Run the spiders asynchronously
@defer.inlineCallbacks
def crawl():
    yield runner.crawl(GriffithGoodLinkSpider)
    yield runner.crawl(GriffithArticleFetchSpider)

    reactor.stop()


crawl()
reactor.run()
