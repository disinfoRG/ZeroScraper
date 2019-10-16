# Import Elasticsearch package
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
from datetime import datetime

# Connect to the elastic cluster
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])


# 1. create a new document
es.create(index='sites', id='N3', body={'url': 'https://', 'name': 'haha tai'})
# 2. get a document
doc = es.get(index='sites', id='N3')
print(doc)
content = doc['_source'] # document contents
print(content)

# 3. bulk add
data = [{'_index': 'news', '_id': '1', 'url': 'http://www.cnba.live/show/202693', 'date': '2019-10-16',
         'title': '特朗普：拆除華為設備！英國：我要7年！歐盟：思科有後門', 'scrape_time': datetime.now(),
         'previous': []},
        {'_index': 'news', '_id': '2', 'url': 'http://www.cnba.live/show/202665', 'date': '2019-10-16',
         'title': '中國史上唯一被做成「臘肉」的皇帝，還霸占了個專屬詞彙「帝羓」', 'scrape_time': datetime.now(),
         'previous': []}]

bulk(es, data)

# 4. update document -- '_version' will increment & original content will be rewritten and erased
update_dict = {'content': updated_content, 'update_time': datetime.now()}
es.update(index='news', id='1', body={'doc': update_dict})

# 5. store older versions within the same document
current_doc = es.get('news', '2')['_source']
previous_version = current_doc['previous']
keys_to_update = ('content', 'scrape_time')
previous_version.append({k: current_doc[k] for k in keys_to_update if k in current_doc}) # move current doc to previous
updated_dict = {'content': new_article, 'scrape_time': datetime.now(), 'previous': previous_version}
es.update(index='news', id='2', body={'doc': update_dict})



