import requests
import bs4
import pandas as pd
import newspaper

def guardian(section, page):
    if page:
        url = 'https://www.theguardian.com/{section}?page={page}'.format(section=section, page=page)
    else:
        url = 'https://www.theguardian.com/{section}'.format(section=section, page=page)
    return url

def get_urls(url):
    r = requests.get(url)
    s = bs4.BeautifulSoup(r.content, 'html5lib')
    for x in s.find_all('li', class_='fc-slice__item'):
        for xx in x.find_all('a', class_='u-faux-block-link__overlay'):
            yield xx['href']

def guardian_hate_url_paginated(page):
    guardian('/society/hate-crime', page)
    return url

def full_text(url):
    a = newspaper.Article(url)
    a.download()
    a.parse()
    return a.text

def scrape(section, outfile, is_hate, pages):
    columns=['url', 'text', 'source', 'label']
    source = 'guardian.com'
    res = []
    cnt = 0
    try:
        for p in pages:
            u = (guardian(section, p))
            print(u)
            for u in get_urls(u):
                print(cnt, u[:50])
                try:
                    txt = full_text(u)
                except newspaper.ArticleException:
                    continue
                res.append([u, txt, source, is_hate])
                cnt += 1
        
    finally:
        df = pd.DataFrame(res, columns=columns)
        df.to_csv(outfile, index=False)

if __name__ == '__main__':
    scrape('society/hate-crime', 'guardian-hate.csv', True, range(1, 8))
    scrape('uk', 'guardian-not_hate-uk.csv', False, [None])
    scrape('us/business', 'guardian-not_hate-us-busines.csv', False, [None])
    scrape('us/environment', 'guardian-not_hate-us-environment.csv', False, [None])
    scrape('uk/business', 'guardian-not_hate-uk-busines.csv', False, [None])
    scrape('world', 'guardian-not_hate-world.csv', False, [None])
    scrape('world/americas', 'guardian-not_hate-world-americas.csv', False, [None])
    
