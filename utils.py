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

class Utils:
    # Create a new folder for saving the fetched files and check whether the folder already exists. If the folder exists, the script will exit
    def create_dir(self, dirname):
        if os.path.exists(dirname):
            return

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
                paths.append(os.path.join(root[len(dirname) :], f))

        return paths

    def exit_on_file_existence(self, filename):
        pass
        # This function should do a lot of validity check in developed assignment. but because we are in
        # deadline of assignment we overwrite the file safely :)

    def exit_on_file_missing(self, filename):
        if not os.path.isfile(filename):
            print(filename,"missing file! choose another file name.")
            sys.exit()


