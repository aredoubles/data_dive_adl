import requests
import bs4
import pandas as pd
import newspaper

def get_urls(url):
    r = requests.get(url)
    s = bs4.BeautifulSoup(r.content, 'html5lib')
    for x in s.find_all('li', class_='fc-slice__item'):
        for xx in x.find_all('a', class_='u-faux-block-link__overlay'):
            yield xx['href']

def guardian_hate_url_paginated(page):
    url = 'https://www.theguardian.com/society/hate-crime?page={page}'.format(page=page)
    return url

def full_text(url):
    a = newspaper.Article(url)
    a.download()
    a.parse()
    return a.text

def main():
    columns=['url', 'text', 'source', 'label']
    source = 'guardian.com'
    label = True
    res = []
    cnt = 0
    try:
        for p in range(1, 8):
            u = (guardian_hate_url_paginated(p))
            print(u)
            for u in get_urls(u):
                print(cnt, u[:50])
                try:
                    txt = full_text(u)
                except newspaper.ArticleException:
                    continue
                res.append([u, txt, source, label])
                cnt += 1
        
    finally:
        df = pd.DataFrame(res, columns=columns)
        df.to_csv('guardian-hate.csv', index=False)

if __name__ == '__main__':
    main()
    
