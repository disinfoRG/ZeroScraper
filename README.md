# NewsScraping
Scrape News contents provided in this [target list](https://airtable.com/tbl3DrYs5mXgl0EV9/viw2cuXweY8OxNkX6?blocks=hide).

### Running
1. Find new articles for sites listed in [url_map.csv](Data/url_map.csv) and store to mysql database on middle2.
```sh
$ cd Codes/newsSpiders
$ python execute_spiders.py --discover --site_id <site_id> 
```
2. Revisit news articles in database based on next_snapshot_at parameter in Article Table on the mysql database. 
The function will save new html to ArticleSnapshot table and update the snapshot parameters in Article Table.
```sh
$ cd Codes/newsSpiders
$ python execute_spiders.py --update
```

### Note:
To successfully connect to mysql db, please create a json file named `db_auth.json` following the same format as [sample_db_auth.json](Data/sample_db_auth.json), and put in `Data` folder. The format is as followed: `mysql://{db_username}:{db_pass}@{db_endpoint}/{db_name}`
