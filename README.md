# NewsScraping
Scrape News contents provided in this [target list](https://airtable.com/tbl3DrYs5mXgl0EV9/viw2cuXweY8OxNkX6?blocks=hide).

### Running

We use MySQL.  To setup database connections, copy `.env.default` to `.env`, and set `DB_URL` value.  MySQL connection string should start with `mysql+pymysql://` so that sqlalchemy uses the correct driver.

We use Python 3.7.  Install Python dependencies and run database migrations:

```sh
$ pip install pipenv
$ pipenv install
# start a shell in virtual env
$ pipenv run alembic upgrade head
```

Then update your site table.  You need an API key from Airtable generated [here](https://airtable.com/account).  Add `API_KEY=<your_api_key>` to `.env`, and then:

```sh
$ cd airtable
$ pipenv run scrapy runspider airtable/spiders/updateSites.py
```

1. To find new articles for a single site listed in Site table in database and store general info to Article and raw html to ArticleSnapshot table:

```sh
$ cd codes
$ python execute_spiders.py --discover --site_id {site_id}
```
    Optional Arguments:
        --depth: maximum search depth limit. default = 0, i.e. no limit.
        --delay: delay time between each request. default = 1.5 (sec)
        --ua: user agent string. default is the latest chrome (v78) user-agent string.

2. To find new articles for all ACTIVE sites listed in Site table in database. Activity is determined by 'is_active' column in Site table.
 ```sh
$ cd codes
$ python batch_discover.py
```

    No optional argument.
    Site-specific arguments (depth, delay, and ua) should be specified in 'config' column of Site table.
    Otherwise the default values will be used.

3. Revisit news articles in database based on next_snapshot_at parameter in Article Table on the mysql database.
The function will save new html to ArticleSnapshot table and update the snapshot parameters in Article Table.
```sh
$ cd codes
$ python execute_spiders.py --update
```
    Optional Arguments:
            --delay: delay time between each request. default = 1.5 (sec)
            --ua: user agent string.

## Development

We use Python 3.7.  Install Python dependencies with pipenv:

```sh
$ pip install pipenv
$ pipenv install --dev
$ pipenv shell

# install pre-commit hooks before hacking for the first time
$ pre-commit install
```
