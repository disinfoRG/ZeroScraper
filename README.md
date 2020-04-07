# ZeroScraper
Scraper for news websites, content farms, ptt, and dcard forums.

0archive is scraping websites provided in this [target list](https://airtable.com/tbl3DrYs5mXgl0EV9/viw2cuXweY8OxNkX6?blocks=hide).

You could set up your website list by following the instruction in [AIRTABLE.md](AIRTABLE.md).
### Setup

We use MySQL.  To setup database connections, copy `.env.default` to `.env`, and set `DB_URL` value.  MySQL connection string should start with `mysql+pymysql://` so that sqlalchemy uses the correct driver.

We use Python 3.7.  Install Python dependencies and run database migrations:

```sh
$ pip install pipenv
$ pipenv install
# start a shell in virtual env
$ pipenv run alembic upgrade head
```

Then update your site table.  First, you need an API key from Airtable generated [here](https://airtable.com/account) and the id of your base (see [here](https://airtable.com/api) for info).  Add the following variables to `.env`:
```sh
$ echo AIRTABLE_BASE_ID={id_of_your_airtable_base} >> .env
$ echo AIRTABLE_API_KEY={your_api_key} >> .env
$ echo SITE_TYPES=["{site_type_1}", "{site_type_2}",...] >> .env
```
Afterwards, do the following to update your site table
```sh
$ SCRAPY_PROJECT=sitesAirtable pipenv run scrapy crawl updateSites
```

### Running
1. To find new articles for a single site listed in Site table in database and store general info to Article and raw html to ArticleSnapshot table:

```sh
$ python site.py discover {site-id}
```
    Optional Arguments:
        # crawler config
        --depth: maximum search depth limit. default = 5.
        --delay: delay time between each request. default = 1.5 (sec)
        --ua: user agent string. default is the chrome v78 user-agent string.

        # site config
        --url: url to start with for this crawl
        --article: regex of article url pattern, e.g. '/story/(\d+).html'
        --following: regex of following url pattern, e.g. 'index/(\d\d+).html'

2. To find new articles for all ACTIVE sites listed in Site table in database. Activity is determined by 'is_active' column in airtable.
```sh
$ python ns.py discover
```

    Optional Arguments:
            --limit-sec: time limit to run in seconds

    Site-specific arguments (depth, delay, and ua) should be specified in 'config' column of Site table.
    Otherwise the default values will be used.

3. Revisit news articles in database based on next_snapshot_at parameter in Article Table on the mysql database.
The function will save new html to ArticleSnapshot table and update the snapshot parameters in Article Table.
```sh
# update all articles
$ python ns.py update
```
    Optional Arguments:
            --limit-sec: time limit to run in seconds


4. Revisit news articles in a specified site.
```sh
$ python site.py update {site-id}
```
    Optional Arguments:
            --delay: delay time between each request. default = 1.5 (sec)
            --ua: user agent string.

5. Revisit one article regardless of next_snapshot_time or snapshot_count.
```sh
$ python article.py update {article-id}
```
    Optional Arguments:
            --selenium: use selenium to load the article.

6. Discover a new article that does not exist in DB based on a provided url.
```sh
$ python article.py discover {url}
```
    Optional Arguments:
            --site-id: id of site of which the url belongs to. default = 0
            --selenium: use selenium to load the article.


## Development

We use Python 3.7.  Install Python dependencies with pipenv:

```sh
$ pip install pipenv
$ pipenv install --dev
$ pipenv shell

# install pre-commit hooks before hacking for the first time
$ pre-commit install
```
## API
### Using Command-line tools
1. Login first: `python ns-api.py login`, if successful, the credential would be saved in `secrets.json`.  
2. To get site stats:
```sh
$ python ns-api.py stats
```
    Optional Arguments:
            --site-id: view stats of a particular site. 
            --date: view stats of a particular date. e.g. 2020-04-03
            -o / --output: filename to save the json output.

3. To get variable:
```sh
$ python ns-api.py variable {variable-key}
```
    Optional Arguments:
            -o / --output: filename to save the json output.


### Using Browser
1. login first: `GET /login` to fill out the form and submit.

### API endpoints  
- Retrieve article info with article_id: `GET /articles/{article_id}`
- Retrieve article info with url, only for exact match: `GET /articles?url={url}`
- Retrieve publication by matching string in title and content: `GET /publications?q={string}`
- Get active sites: `GET /sites/active`
- Get total article count in a site: `GET /sites/{site_id}/article_count`
- Get new articles in a site discovered during a time interval: `GET /sites/{site_id}/new_articles?timeStart={unix_time}&timeEnd={unix_time}`
- Get articles in a site updated during a time interval: `GET /sites/{site_id}/updated_articles?timeStart={unix_time}&timeEnd={unix_time}`
- Get article discovered most recently in a site: `GET /sites/{site_id}/latest_article`
- Get stats of a site: `GET /stats?site_id={site_id}`
- Get stats of a day: `GET /stats?date={date}`
- Get all stats: `GET /stats`
- Get health: `GET /health`
- Get variable: `GET /variable?key={variable-key}`


## Dump snapshot table

```sh
$ ns-dump.py --table ArticleSnapshotYYYYMM --output YYYYMM.jsonl
```
