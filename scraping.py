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


# definition of a first scrapy spider used to retrieve the content of each url and save it to a local file
class GriffithArticleFetchSpider(scrapy.Spider):
    name = "griffith_articles_fetch"
    allowed_domains = ["https://www.griffith.ie", "www.griffith.ie"]
    start_urls = urls
    counter = 1

    def parse(self, response):
        result = str(
            w3lib.html.replace_tags(
                str(response.css(".basic-page__content").getall()), "  "
            )
        )
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


class ScrapeUtils:
    # Create a new folder for saving the fetched files and check whether the folder already exists. If the folder exists, the script will exit
    def create_dir(self, dirname):
        if os.path.exists(dirname):
            print("folder you specified already exists! Please remove it first")
            sys.exit()

        os.makedirs(dirname)

    def parse_args(self, expected, message):
        if len(sys.argv) != expected + 1:
            print("Error, Usage:", message)
            sys.exit()
        if expected == 1:
            return sys.argv[1]
        if expected == 2:
            return sys.argv[1], sys.argv[2]
        if expected == 3:
            return sys.argv[1], sys.argv[2], sys.argv[3]
        if expected == 3:
            return sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4]



    # Run the spiders asynchronously
    @defer.inlineCallbacks
    def crawl(self, runner):
        yield runner.crawl(GriffithGoodLinkSpider)
        yield runner.crawl(GriffithArticleFetchSpider)

        reactor.stop()

    # function taking the path of a folder as an argument and returning the list of paths of files in the folder whose names begin with D
    def dir_files_path(self, dirname):
        paths = []
        if not os.path.exists(dirname):
            print("No Directory named " + dirname)
            sys.exit()

        for root, _, files in os.walk(dirname):
            for f in files:
                if f.startswith("D"):
                    paths.append(os.path.join(root[len(dirname) :], f))

        return paths

    def exit_on_file_existence(self, filename):
        if os.path.isfile(filename):
            print(filename,"exists! choose another file name.")
            sys.exit()

    def exit_on_file_missing(self, filename):
        if not os.path.isfile(filename):
            print(filename,"missing file! choose another file name.")
            sys.exit()

def main():
    dirname = ScrapeUtils().parse_args(1, "python scrapping.py <outfolder>")
    ScrapeUtils().create_dir(dirname)

    settings = get_project_settings()
    configure_logging(settings)
    runner = CrawlerRunner(settings)

    ScrapeUtils().crawl(runner)
    reactor.run()


if __name__ == "__main__":
    main()
