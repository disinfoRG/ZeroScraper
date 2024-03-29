
# ZeroScraper

Scraper for news websites, content farms, ptt, and dcard forums.

0archive is scraping websites provided in this [target list](https://airtable.com/tbl3DrYs5mXgl0EV9/viw2cuXweY8OxNkX6?blocks=hide).

You could set up your website list by following the instruction in [AIRTABLE.md](AIRTABLE.md).

## Setup

We use MySQL.  To setup database connections, copy `.env.default` to `.env`, and change `DB_URL` to your connection string.  The connection string should start with `mysql+pymysql://` so that sqlalchemy uses the correct driver.

We use Python 3.7, and Pipenv to manage Python packages.  Install Python packages with:

```sh
$ pip install pipenv
$ pipenv install
```

The database table of all websites can get updates from Airtable, if you followed above instructions to setup one.  You need an API key from Airtable (generate yours [here](https://airtable.com/account)), and the id of your base (find yours [here](https://airtable.com/api)).  Then add the following variables to `.env`:

```sh
AIRTABLE_BASE_ID={id_of_your_airtable_base}
AIRTABLE_API_KEY={your_api_key}
SITE_TYPES=["{site_type_1}", "{site_type_2}",...]
```

Then, run the following commands to finish the setup:

```sh
$ pipenv shell          # start a shell in the virtual env
$ invoke migrate        # run database migrations
$ invoke update-sites   # update your site table
```

## Run

The following commands assume that you're in the virtual env.  Run `pipenv shell` before start.

0. Make sure you have a list of websites to crawl:

   ```sh
   python zs-site.py list
   ```

1. Find new articles for a single site listed in Site table in database and store general info to Article and raw html to ArticleSnapshot table:

   ```sh
   $ python zs-site.py discover {site-id}
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

2. Find new articles for all ACTIVE sites listed in Site table in database. Activity is determined by 'is_active' column in airtable.

   ```sh
   $ python zs.py discover
   ```

        Optional Arguments:
                --limit-sec: time limit to run in seconds
    
        Site-specific arguments (depth, delay, and ua) should be specified in 'config' column of Site table.
        Otherwise the default values will be used.

3. Revisit articles in database based on next_snapshot_at parameter in Article Table on the mysql database.
   The function will save new html to ArticleSnapshot table and update the snapshot parameters in Article Table.

   ```sh
   # update all articles
   $ python zs.py update
   ```
        Optional Arguments:
                --limit-sec: time limit to run in seconds


4. Revisit articles in a specified site.

   ```sh
   $ python zs-site.py update {site-id}
   ```
        Optional Arguments:
                --delay: delay time between each request. default = 1.5 (sec)
                --ua: user agent string.

5. Revisit one article regardless of next_snapshot_time or snapshot_count.

   ```sh
   $ python zs-article.py update {article-id}
   ```
        Optional Arguments:
                --selenium: use selenium to load the article.

6. Discover a new article that does not exist in DB based on a provided url.

   ```sh
   $ python zs-article.py discover {url}
   ```
        Optional Arguments:
                --site-id: id of site of which the url belongs to. default = 0
                --selenium: use selenium to load the article.


## Hack

We use Python 3.7, and Pipenv to manage Python packages.  Install Python packages with:

```sh
$ pip install pipenv
$ pipenv install --dev
# only the first time
$ pre-commit install
```

Generally following the way [Scrapy](https://scrapy.org/) projects are structured, ZeroScraper consists of the following components:

* `newsSpiders`: the main scraper project.
* `sitesAirtable`: the scraper project that updates websites table using Airtable data.
* `migrations`: database migrations.
* `queries`: some commonly used SQL queries.
* `jobqueue`: a job queue using MySQL as storage to coordinate data pipeline.
* `tests`: tests.
* There is a [web api](API.md) implemented under `newsSpiders/webapi`.

## Operate

### Dump snapshot table

```sh
$ zs-dump.py --table ArticleSnapshotYYYYMM --output YYYYMM.jsonl
```
