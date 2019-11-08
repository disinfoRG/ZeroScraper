# NewsScraping
Scrape News contents provided in this [target list](https://airtable.com/tbl3DrYs5mXgl0EV9/viw2cuXweY8OxNkX6?blocks=hide).

### Running
```sh
$ cd Codes/newsSpiders
```
1. Find new articles for sites listed in [url_map.csv](Data/url_map.csv). The new article metadata will be appended to the jsonlines file [article.jsonl](Data/article.jsonl) and html will be appended to [article_snapshot.jsonl](Data/article_snapshot.jsonl)
```
$ python execute_spiders.py --discover --site_id <site_id> 
```
2. Revisit news articles in database based on next_fetch_at parameter in [article.jsonl](Data/article.jsonl). 
The function will save new html to [article_snapshot.jsonl](Data/article_snapshot.jsonl) and (_ideally but not yet implemented_) update the versioning parameters in [article.jsonl](Data/article.jsonl)
```
$ python execute_spiders.py --update --site_id <site_id>
```

### To-dos and Comments
>1. the update function is not complete yet -- it currently stores article snapshots but does not update the original 
article list for arguments such as fetch_count and next_fetch_date. Might wait for database connection.

>2. need a way to store update frequency for different online content and find a way to connect with the spider so 
crawl frequency parameters (such as next_fetch_at and fetch_count) could be updated.