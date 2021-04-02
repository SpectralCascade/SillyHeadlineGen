import scrapy
from pandas import read_csv
from readability.readability import Document

PATH_TO_DATA = "list of urls"  # csv list of urls to look through


class HeadlineSpider(scrapy.Spider):  # CLass for scraping headlines
    name = "headlines"
    start_urls = read_csv(PATH_TO_DATA).url.tolist()  # opens the csv of urls to scrape

    def parse(self, response):  # main function of the spider
        doc = Document(response.text)  # parses html so it is easier to handle
        yield {  # returns whatever values are put in the brackets
            'title': doc.title(),  # adds title column into the spreadsheet output
            'url': response.url  # adds url column into the spreadsheet output
        }
