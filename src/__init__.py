from src.controller import WebScrapingController
from src.model import WebScraper
import doctest

if __name__ == "__main__":
    #doctest.testfile("doctest.txt")
    cs = WebScrapingController(WebScraper())
    cs.go()
