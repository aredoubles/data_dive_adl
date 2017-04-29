import requests
import bs4
import feedparser


# NY Times Hate Crimes feed
def nyt_hate():
    nytrss = feedparser.parse(
        'https://www.nytimes.com/svc/collections/v1/publish/http://www.nytimes.com/topic/subject/hate-crimes/rss.xml')

    for i in range(20):
        res = requests.get(nytrss['entries'][i]['link'])
        res.raise_for_status()
        starch = bs4.BeautifulSoup(res.text, 'html5lib')
        # The below is specific to the NYT
        thetext = starch.find_all(class_='story-body-text')

        with open("Output.txt", "a") as text_file:
            for tag in thetext:
                text_file.write(tag.text.strip())
                text_file.write(' ')

            # Insert a line break after each article
            text_file.write('\n\n')


# NY Times feed on NY local news
def nyt_loca():
    nytrss = feedparser.parse(
        'https://www.nytimes.com/svc/collections/v1/publish/https://www.nytimes.com/section/nyregion/rss.xml')

    for i in range(20):
        res = requests.get(nytrss['entries'][i]['link'])
        res.raise_for_status()
        starch = bs4.BeautifulSoup(res.text, 'html5lib')
        # The below is specific to the NYT
        thetext = starch.find_all(class_='story-body-text')

        with open("Output.txt", "a") as text_file:
            for tag in thetext:
                text_file.write(tag.text.strip())
                text_file.write(' ')

            # Insert a line break after each article
            text_file.write('\n\n')
