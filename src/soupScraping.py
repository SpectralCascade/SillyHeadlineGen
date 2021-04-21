import requests
from bs4 import BeautifulSoup
import csv
import CV from CV

def categoriseArticle(headline, content):
    cv_map = dict()
    
    region = "Region"
    cv_map[region] = dict()
    with open("data/Countries-Continents.csv") as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            
    for term in CV[region]:
        cv_map[region][term] = dict()

def chaserScrape():
    for i in range(10):
        url = (f'https://chaser.com.au/news/page/{i}/')
        page = requests.get(url)
        soup1 = BeautifulSoup(page.content, 'html.parser')

        with open('chaserHeadlines.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            headlines = soup1.find_all('div', {'class': 'archive_story_title'})
            for headline in headlines:
                headlineString = headline.text
                writer.writerow([headlineString])


def dailymashScrape():
    for i in range(10):
        url = (f'https://www.thedailymash.co.uk/news/page/{i}')
        page = requests.get(url)
        soup1 = BeautifulSoup(page.content, 'html.parser')

        with open('dailymashHeadlines.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            headlines = soup1.find_all('div', {'class': 'holder'})
            for headline in headlines:
                headlineStripped = headline.find_all('a')
                for headline2 in headlineStripped:
                    headlineString = headline2.text
                    writer.writerow([headlineString])


def beavertonScrape():
    for i in range(10):
        url = (f'https://www.thebeaverton.com/news/world/page/{i}')
        page = requests.get(url)
        soup1 = BeautifulSoup(page.content, 'html.parser')

        with open('beavertonHeadlines.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            headlines = soup1.find_all('header', {'class': 'post-title entry-header'})
            for headline in headlines:
                print(headline)
                headlineStripped = headline.find_all('h3')
                for headline2 in headlineStripped:
                    headlineString = headline2.text
                    writer.writerow([headlineString])
