from libs.crawler import Crawler

from config import *

def run() :
    crawler = Crawler()
    crawler.run(seed_url)


if __name__ == "__main__" :
    run()