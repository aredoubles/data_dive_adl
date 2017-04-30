import newspaper
import pandas as pd

urls = open('nyt-hate-urls.txt')
urls = [x.rstrip() for x in urls]


def full_text(url):
    a = newspaper.Article(url)
    a.download()
    a.parse()
    return a.text

def main():
    columns=['url', 'text', 'source', 'label']
    source = 'nytimes.com'
    label = True
    res = []
    cnt = 0
    try:
        for u in urls:
            print(cnt, u[:50])
            try:
                txt = full_text(u)
            except newspaper.ArticleException:
                continue
            res.append([u, txt, source, label])
            cnt += 1
        
    finally:
        df = pd.DataFrame(res, columns=columns)
        df.to_csv('nyt-hate.csv', index=False)

if __name__ == '__main__':
    main()
    
