# NewsScraping
Scrape News contents provided in this [target list](https://airtable.com/tbl3DrYs5mXgl0EV9/viw2cuXweY8OxNkX6?blocks=hide).

### Running

We use MySQL.  To setup database connections:

1. Copy `.env.default` to `.env`, and set `DB_URL` value.  Start the MySQl connection string with `mysql+pymysql://` so that sqlalchemy uses the correct driver.

We use Python 3.7.  Install Python dependencies and run database migrations:

```sh
$ pip install pipenv
$ pipenv install
# start a shell in virtual env
$ pipenv shell
# run db migrations
$ alembic upgrade head
```

Then,

1. Find new articles for sites listed in Site table in database and store general info to Article and raw html to ArticleSnapshot table.
```sh
$ cd codes
$ python execute_spiders.py --discover --site_id {site_id}
```
2. Revisit news articles in database based on next_snapshot_at parameter in Article Table on the mysql database.
The function will save new html to ArticleSnapshot table and update the snapshot parameters in Article Table.
```sh
$ cd codes
$ python execute_spiders.py --update
```

## Development

We use Python 3.7.  Install Python dependencies with pipenv:

```sh
$ pip install pipenv
$ pipenv install --dev
$ pipenv shell

# install pre-commit hooks before hacking for the first time
$ pre-commit install
```
