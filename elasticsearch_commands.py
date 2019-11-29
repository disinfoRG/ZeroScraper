from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk, scan
from datetime import datetime

# Connect to the elastic cluster
es_url = "your elasticsearch database url"
es = Elasticsearch(es_url)
# or, connect with local es database:
# es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

# 1. create a new document
es.create(
    index="sites",
    id="N3",
    doc_type="_doc",
    body={"url": "https://", "name": "haha tai"},
)

# 2. get a document
doc = es.get(index="sites", id="N3")  # or specify doc type
print(doc)
content = doc["_source"]  # document contents
print(content)

# 3. bulk add
data = [
    {
        "_index": "news",
        "_id": "1",
        "url": "http://www.cnba.live/show/202693",
        "date": "2019-10-16",
        "title": "特朗普：拆除華為設備！英國：我要7年！歐盟：思科有後門",
        "scrape_time": datetime.now(),
        "previous": [],
    },
    {
        "_index": "news",
        "_id": "2",
        "url": "http://www.cnba.live/show/202665",
        "date": "2019-10-16",
        "title": "中國史上唯一被做成「臘肉」的皇帝，還霸占了個專屬詞彙「帝羓」",
        "scrape_time": datetime.now(),
        "previous": [],
    },
]

bulk(es, data)

# 4. update document -- '_version' will increment & original content will be rewritten and erased
update_dict = {"content": updated_content, "update_time": datetime.now()}
es.update(index="news", id="1", body={"doc": update_dict})

# 5. store older versions within the same document
current_doc = es.get("news", "2")["_source"]
previous_version = current_doc["previous"]
keys_to_update = ("content", "scrape_time")
previous_version.append(
    {k: current_doc[k] for k in keys_to_update if k in current_doc}
)  # move current doc to previous
updated_dict = {
    "content": new_article,
    "scrape_time": datetime.now(),
    "previous": previous_version,
}
es.update(index="news", id="2", body={"doc": update_dict})

# 6. delete
# delete index
index = "sites"
es.indices.delete(index)
# delete document
es.delete(index=index, id="1")
# 7. search query
# search all
search_query = {"query": {"match_all": {}}}
res = es.search(size=10000, index="news", body=search_query)
print(len(res["hits"]["hits"]))  # num of documents
i = 0
print(res["hits"]["hits"][i])  # single documents

# conditional search
search_query = {"query": {"match": {"date": "2019-10-16"}}}

# use helpers.scan to search
# https://elasticsearch-py.readthedocs.io/en/master/helpers.html#elasticsearch.helpers.scan
search_generator = scan(es, query=search_query, index="news")
# size of search results
print(sum(1 for _ in search_generator))

#### REST API ####
import requests
import json

es_url = "your elasticsearch database url"

# A. Document Level
# A1. retrieve data -> GET request
r = requests.get(f"{es_url}/{index}/{document_id}")
r.json()

# A2. modify data of a document -> PUT request
modified_data = {"name": "andrea"}
requests.put(f"{es_url}/{index}/{document_id}", data=json.dumps(modified_data))

# A3. add new data to an index -> POST request (automatically create index if first time)
new_data = {"name": "andrea", "sex": "female"}
r = requests.post(f"{es_url}/{index}", data=json.dumps(new_data))
print(r.json()["_id"])

# A4. Delete -> DELETE request
requests.delete(f"{es_url}/{index}/{document_id}")

# A5. Bulk add
json = '{"index": {"_type": "sites"}}\n {"site_name": "udn2", "site_url": "https://udn.com.tw"}\n {"index": {"_type": "sites"}}\n {"site_name": "cctv2", "site_url": "https:/cctv.com.cn"}'
r = requests.post(f"{es_url}/_bulk", data=json)

# B. Index Level
# B1. search every record in an index
r = requests.get(f"{es_url}/{index}/_search?")
doc_list = r.json()["hits"]["hits"]
# B2. special search
search_query = {"query": {"match": {"site_name": "qiqi"}}}
doc_list = r.json()["hits"]["hits"]
