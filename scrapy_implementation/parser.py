from bs4 import BeautifulSoup
import json

article_js = json.load(open('../../Data/ArticleSnapshot.json', 'rb'))
for article in article_js:
    soup = BeautifulSoup(article['raw_body'], 'html5lib')
    if article['from_site'] == 'N1':
        # get title
        title = soup.find('h1').text
        # get content
        content = ' '.join([x.text for x in soup.find(True, {'id': 'contentArea'}).find_all('p')]).replace('\u3000', '').strip()
        # save to article content

