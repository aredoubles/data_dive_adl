import requests
import bs4
import feedparser
import pandas as pd
import LocalCrawl


# NY Times Hate Crimes feed
def nyt_hate():
    nytrss = feedparser.parse(
        'https://www.nytimes.com/svc/collections/v1/publish/http://www.nytimes.com/topic/subject/hate-crimes/rss.xml')

    nythate = {}
    for i in range(10):
        idlink = nytrss['entries'][i]['link']
        res = requests.get(nytrss['entries'][i]['link'])
        res.raise_for_status()
        starch = bs4.BeautifulSoup(res.text, 'html5lib')
        # The below is specific to the NYT
        thetext = starch.find_all(class_='story-body-text')

        full = ''
        for tag in thetext:
            full += (tag.text.strip() + ' ')

        nythate[idlink] = full

    build = pd.DataFrame.from_dict(nythate, orient='index')
    build.columns = ['Text']
    build['Source'] = 'New York Times'
    build['Hate crime'] = 1
    build.index.names = ['URL']
    build.to_csv('NYT1.csv')

    return build


# NY Times feed on NY local news
def nyt_local():
    nytrss = feedparser.parse(
        'https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/nyregion/rss.xml')

    nytnon = {}
    for i in range(10):
        idlink = nytrss['entries'][i]['link']
        res = requests.get(nytrss['entries'][i]['link'])
        res.raise_for_status()
        starch = bs4.BeautifulSoup(res.text, 'html5lib')
        # The below is specific to the NYT
        thetext = starch.find_all(class_='story-body-text')

        full = ''
        for tag in thetext:
            full += (tag.text.strip() + ' ')

        nytnon[idlink] = full

    build = pd.DataFrame.from_dict(nytnon, orient='index')
    build.columns = ['Text']
    build['Source'] = 'New York Times'
    build['Hate crime'] = 0
    build.index.names = ['URL']
    build.to_csv('NYT0.csv')

    return build


# Guardian feed on hate crime
def guardian_hate():
    guardrss = feedparser.parse(
        'https://www.theguardian.com/society/hate-crime/rss')

    guardhate = {}
    for i in range(20):
        idlink = guardrss['entries'][i]['link']
        res = requests.get(guardrss['entries'][i]['link'])
        res.raise_for_status()
        starch = bs4.BeautifulSoup(res.text, 'html5lib')
        # The below is specific to The Guardian
        thetext = starch.find_all('div', itemprop='articleBody')

        for tag in thetext:
            string = tag.text.strip()
            string = string.replace('\r', ' ').replace('\n', ' ')
            full = string

        guardhate[idlink] = full

    build = pd.DataFrame.from_dict(guardhate, orient='index')
    build.columns = ['Text']
    build['Source'] = 'The Guardian'
    build['Hate crime'] = 1
    build.index.names = ['URL']
    build.to_csv('Guardian1.csv')

    return build


def guardian_uk():
    guardrss = feedparser.parse(
        'https://www.theguardian.com/uk-news/rss')

    guarduk = {}
    for i in range(20):
        idlink = guardrss['entries'][i]['link']
        res = requests.get(guardrss['entries'][i]['link'])
        res.raise_for_status()
        starch = bs4.BeautifulSoup(res.text, 'html5lib')
        # The below is specific to The Guardian
        thetext = starch.find_all('div', itemprop='articleBody')

        for tag in thetext:
            string = tag.text.strip()
            string = string.replace('\r', ' ').replace('\n', ' ')
            full = string

        guarduk[idlink] = full

    build = pd.DataFrame.from_dict(guarduk, orient='index')
    build.columns = ['Text']
    build['Source'] = 'The Guardian'
    build['Hate crime'] = 0
    build.index.names = ['URL']
    build.to_csv('Guardian0.csv')

    return build


if __name__ == '__main__':
    nyt1 = nyt_hate()
    nyt0 = nyt_local()
    grd1 = guardian_hate()
    grd0 = guardian_uk()
    local1 = LocalCrawl.localart()
    articles = pd.concat([nyt1, nyt0, grd1, grd0, local1])
    articles.to_csv('Articles.csv')
