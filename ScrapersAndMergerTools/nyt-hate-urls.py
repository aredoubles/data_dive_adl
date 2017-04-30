import bs4

# workflow
# 1. open 'https://www.nytimes.com/topic/subject/hate-crimes' in browser and
#    click more articles and scroll down untile you see enough articles.  This 
#    will fetch the infinet scroll of articles.
# 2. save as html in your browser to a local file and run the following code to
#    extract the urls.
# 3. update the following line to the file name of the download.
f = 'Hate Crimes - The New York Times.html'
f = open(f).read()
s = bs4.BeautifulSoup(f)
div = s.find('div', class_='stream')
q = div.find_all('a', class_='story-link')
urls = [x['href'] for x in q]
out = open('nyt-hate-urls.txt', 'w')
for u in urls:
    print(u, file=out)
    
