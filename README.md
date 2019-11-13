
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
