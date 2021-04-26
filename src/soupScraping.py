import requests
from bs4 import BeautifulSoup
import csv
import string


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
            writer = csv.writer(file)
            headlines = soup1.find_all('div', {'class': 'holder'})
            for headline in headlines:
                headlineStripped = headline.find_all('a')
                for headline2 in headlineStripped:
                    headlineString = headline2.text
                    writer.writerow([headlineString])
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


def newYTScrape():

    all_headlines = []
    #categorisedHeadlines = {"Europe": [],
                            #"Asia": [],
                            #"Africa": [],
                            #"North America": [],
                            #"South America": [],
                            #"Oceania": [],
                            #"Entertainment": [],
                            #"Food": [],
                            #"Health": [],
                            #"Sport": [],
                            #"Politics": []}

    categorisedHeadlines = {"Europe": [],
                            "Asia": [],
                            "Africa": [],
                            "North America": []}

    #categories = {"Europe", "Asia", "Africa", "North America", "South America", "Oceania", "Entertainment", "Food", "Health", "Sport", "Politics"}
    categories = {"Europe", "Asia", "Africa", "North America"}
    apikey = "GLCfr8MOODZHWK3UoGDVB1HAXNR1rzPA"
    begin_date = "20210201"
    for category in categories:
        #for headline in all_headlines:
            #print(headline)
        #input()
        url = f"https://api.nytimes.com/svc/search/v2/articlesearch.json?" \
            f"q={category}" \
            f"&api-key={apikey}" \
            f"&begin_date={begin_date}" \

        r = requests.get(url)
        #print(r.json())
        for dict in r.json()['response']['docs']:
            categorisedHeadlines[category].append([dict['headline']['main']])
            all_headlines.append(dict['headline']['main'])

    #for headline in categorisedHeadlines:
        #print(headline[0])
    print(categorisedHeadlines["Europe"])
    print(categorisedHeadlines["Asia"])
    print(categorisedHeadlines["Africa"])
    print(categorisedHeadlines["North America"])
    return(all_headlines)





newYTScrape()
