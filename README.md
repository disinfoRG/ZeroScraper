# NewsScraping
Scrape News contents provided in this [target list](https://airtable.com/tbl3DrYs5mXgl0EV9/viw2cuXweY8OxNkX6?blocks=hide).

### Running
1. Find new articles for sites listed in [url_map.csv](Data/url_map.csv). The new article metadata will be appended to the jsonlines file [article.jsonl](Data/article.jsonl) and html will be appended to [article_snapshot.jsonl](Data/article_snapshot.jsonl)
```sh
$ cd Codes/newsSpiders
$ python execute_spiders.py --discover --site_id <site_id> 
```
2. Revisit news articles in database based on next_fetch_at parameter in [article.jsonl](Data/article.jsonl). 
The function will save new html to [article_snapshot.jsonl](Data/article_snapshot.jsonl) and (_ideally but not yet implemented_) update the versioning parameters in [article.jsonl](Data/article.jsonl)
```sh
$ cd Codes/newsSpiders
$ python execute_spiders.py --update
```

### Note:
To successfully connect to mysql db, please create db_auth.json in Data/ following the same format as [sample_db_auth.json](Data/sample_db_auth.json).
