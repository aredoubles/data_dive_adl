import requests
import bs4
import pandas as pd
import newspaper

def get_urls(url):
    r = requests.get(url)
    s = bs4.BeautifulSoup(r.content, 'html5lib')
    for x in s.find_all('div', class_='ez-main'):
        yield x.find('a', class_='ez-title')['href']

def abc_hate_urls():
    url = 'http://abcnews.go.com/topics/news/issues/hate-crimes.htm'
    print(url)
    r = requests.get(url)
    s = bs4.BeautifulSoup(r.content, 'html5lib')
    for x in s.find_all('div', class_='ez-main'):
        yield x.find('a', class_='ez-title')['href']

def abc_hate_url_paginated(page):
    start = page*10
    url = 'http://abcnews.go.com/topics/topic-more-results-pagelet?pageid=883548&start={start}&page={page}&mediatype=&_=1493505341937'.format(page=page, start=start)
    return url

def full_text(url):
    a = newspaper.Article(url)
    a.download()
    a.parse()
    return a.text

def main():
    columns=['url', 'text', 'source', 'label']
    source = 'abcnews.com'
    label = True
    res = []
    cnt = 0
    try:
        for p in range(1, 101):
            u = (abc_hate_url_paginated(p))
            for u in get_urls(u):
                print(cnt, u[:50])
                txt = full_text(u)
                res.append([u, txt, source, label])
                cnt += 1
    except newspaper.ArticleException:
        pass
    finally:
        df = pd.DataFrame(res, columns=columns)
        df.to_csv('abc-hate.csv', index=False)

if __name__ == '__main__':
    main()
    
