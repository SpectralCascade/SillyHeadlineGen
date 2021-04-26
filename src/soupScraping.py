import requests
from bs4 import BeautifulSoup
import csv
import string
import math
import sys

def categoriseArticle(headline, content):
    categories = dict()
    cv_map = dict()

    region = "Region"
    cv_map[region] = dict()
    with open("data/Countries-Continents.csv") as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)
        for row in reader:
            if (row[0] not in cv_map[region]):
                cv_map[region][row[0]] = dict()
            cv_map[region][row[0]][row[1]] = 1

    # Extract words from article headline and content
    # TODO: extract full subjects/objects/nouns so full country names work
    words = []
    for word in headline.split():
        word = word.translate(str.maketrans('', '', string.punctuation))
        words.append(word)
    for word in content.split():
        word = word.translate(str.maketrans('', '', string.punctuation))
        words.append(word)

    # Top level terms (i.e. Region, Culture and Subject)
    for word in words:
        for key in cv_map:
            terms = cv_map[key]
            if (word in terms):
                if (word not in categories):
                    categories[word] = 1
                categories[word] += 1
                break
            # Inner terms, e.g. Europe, Africa, Asia
            # with subterms e.g. Spain, Portugal, France
            for inner_terms in terms:
                subterms = terms[inner_terms]
                if (word in subterms):
                    if (word not in categories):
                        categories[term] = 1
                    categories[word] += 1
                break

    return categories


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


# TODO: extract article contents
def dailymashScrape(max_headlines):
    num = 0
    all_headlines = []
    for i in range(100):
        url = (f'https://www.thedailymash.co.uk/news/page/{i}')
        page = requests.get(url)
        soup1 = BeautifulSoup(page.content, 'html.parser')

        print("\nPage " + str(i) + "\n")
        with open('dailymashHeadlines.csv', 'a', newline='') as file:
            #writer = csv.writer(file)
            headlines = soup1.find_all('div', {'class': 'holder'})
            for headline in headlines:
                headlineStripped = headline.find_all('a')
                for headline2 in headlineStripped:
                    headlineString = headline2.text
                    #writer.writerow([headlineString])
                    # test categorisation
                    #print("Headline: " + headlineString + " | Categories: " + str(categoriseArticle(headlineString, "")))
                    num += 1
                    all_headlines.append(headlineString)
                    if (num >= max_headlines):
                        return all_headlines
    return all_headlines


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

#dailymashScrape(40)


def newYTScrape(max_headlines, category = ""):

    all_headlines = []
    apikey = "GLCfr8MOODZHWK3UoGDVB1HAXNR1rzPA"
    # TODO: convert CV category into valid query term
    query = category
    begin_date = "20001001"

    total_pages = math.ceil(max_headlines / 10)
    count = 0

    for p in range(total_pages):
        url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?" + (f"q={query}&" if not query else f"") + f"api-key={apikey}&begin_date={begin_date}&page={p}"

        print ("Querying NYT database with GET request to " + url)
        r = requests.get(url)
        while ('response' not in r.json()):
            r = requests.get(url)
        for dict in r.json()['response']['docs']:
            if count < max_headlines:
                all_headlines.append(dict['headline']['main'])
            else:
                break
            count += 1

    return all_headlines


def guardianScrape(max_headlines, category=""):
    all_headlines = []
    apikey = "01dfb74a-30e0-468a-a59e-040459e67a38"
    query = category
    begin_date = "2000-10-01"
    total_pages = math.ceil(max_headlines / 10)
    count = 0
    for p in range(total_pages):
        url = f"https://content.guardianapis.com/search?" + f"api-key={apikey}" + f"&query-fields=headline&from-date={begin_date}" + (f"&q={query}" if not query else f"") + f"&page={p+1}"
        print("Querying The Guardian database with GET request to " + url)
        r = requests.get(url)
        if 'response' in r.json():
            for dict in r.json()['response']['results']:
                if count < max_headlines:
                    all_headlines.append(dict['webTitle'])
                else:
                    break
                count += 1

    return all_headlines


if __name__ == "__main__":
    import nlp

    max_scrape = 10000
    adjectives = set()
    with open("data/exclusive_real_adjectives.csv", "w", newline='', encoding='utf-8') as csvfile:
        g_headlines = guardianScrape(max_scrape)
        writer = csv.writer(csvfile, delimiter=',')
        for headline in g_headlines:
            extracted = nlp.GetHeadlineNLP().nlp_extract(headline)
            for adj in extracted["adjectives"]:
                print (adj)
                if adj not in adjectives:
                    adjectives.add(adj)
                    writer.writerow([adj])
    print("Finished output in data/exclusive_real_adjectives.csv")