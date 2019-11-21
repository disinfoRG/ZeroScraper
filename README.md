# NewsScraping
Scrape News contents provided in this [target list](https://airtable.com/tbl3DrYs5mXgl0EV9/viw2cuXweY8OxNkX6?blocks=hide).

### Running
1. Find new articles for sites listed in Site table in database and store general info to Article and raw html to ArticleSnapshot table.
```sh
$ cd Codes
$ python execute_spiders.py --discover --site_id {site_id}
```
2. Revisit news articles in database based on next_snapshot_at parameter in Article Table on the mysql database.
The function will save new html to ArticleSnapshot table and update the snapshot parameters in Article Table.
```sh
$ cd Codes
$ python execute_spiders.py --update
```

### Note:
To successfully connect to mysql db, please create a json file named `db_auth.json` following the same format as [sample_db_auth.json](Data/sample_db_auth.json), and put in `Data` folder. The format is as followed: `mysql://{db_username}:{db_pass}@{db_endpoint}/{db_name}`

## Development

We use Python 3.6.  Install Python dependencies with pipenv:

```sh
$ pip install pipenv
$ pipenv install --dev
$ pipenv shell

# install pre-commit hooks before hacking for the first time
$ pre-commit install
```

Note that if you are using "mysql-client" and "openssl" packages from Homebrew on macOS, you might want to install Python dependencies with the following command:

```sh
PATH="/usr/local/opt/mysql-client/bin:$PATH" \
LDFLAGS="-L/usr/local/opt/openssl/lib" \
CPPFLAGS="-I/usr/local/opt/openssl/include" \
pipenv install --dev
```

We use MySQL.  To setup database connect:

1. Copy `.env.default` to `.env`, and set `DATABASE_URL` value.
2. Copy `alembic.ini.default` to `alembic.ini`, and set `sqlalchemy.url` value.

Then run database migrations:

```sh
# run db migrations
$ alembic upgrade head
```
