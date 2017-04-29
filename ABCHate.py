import requests
import bs4
import pandas as pd
import newspaper

def abc_hate_urls():
    url = 'http://abcnews.go.com/topics/news/issues/hate-crimes.htm'
    print(url)
    r = requests.get(url)
    s = bs4.BeautifulSoup(r.content, 'html5lib')
    for x in s.find_all('div', class_='ez-main'):
        yield x.find('a', class_='ez-title')['href']

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
    for url in abc_hate_urls():
        txt = full_text(url)
        res.append([url, txt, source, label])
    df = pd.DataFrame(res, columns=columns)
    df.to_csv('abc-hate.csv', index=False)

if __name__ == '__main__':
    main()
    
