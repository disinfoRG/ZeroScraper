
0archive
===

## Development

Requires Python 3.6.

```sh
$ pipenv install --dev
$ pipenv shell

# run db migrations
$ alembic upgrade head

# run spiders
$ scrapy crawl "nooho-怒吼文章"

# install pre-commit hooks before hacking for the first time
$ pre-commit install
```

To run it with MySQL, set `DATABASE_URL` in `.env`, and `sqlalchemy.url` in `alembic.ini`.  If you are using MySQL on macOS, you might want to try installing Python dependencies with:

```sh
PATH="/usr/local/opt/mysql-client/bin:$PATH" LDFLAGS="-L/usr/local/opt/openssl/lib" CPPFLAGS="-I/usr/local/opt/openssl/include" pipenv install --dev
```
