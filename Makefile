.PHONY: migrate
migrate:
	alembic upgrade head

.PHONY: updateSites
updateSites:
	SCRAPY_PROJECT=sitesAirtable pipenv run scrapy crawl updateSites
