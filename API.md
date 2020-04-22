ZeroScraper API
===


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
1. authentication
    - login `POST /login?username={username}&password={password}`
    - logout `POST /logout`
1. system monitoring 
    - Get health: `GET /health`
    - Get variable: `GET /variable?key={variable-key}`

1. stats
    - Get all stats: `GET /stats`
    - Get stats of a site: `GET /stats?site_id={site_id}`
    - Get stats of a day: `GET /stats?date={date}`

1. articles
    - Retrieve article info with article_id: `GET /articles/{article_id}`
    - Retrieve article info with url, only for exact match: `GET /articles?url={url}`
1. sites
    - Get all sites: `GET /sites`
    - Get active sites: `GET /sites/active`
    - Get total article count in a site: `GET /sites/{site_id}/article_count`
    - Get new articles in a site discovered during a time interval: `GET /sites/{site_id}/new_articles?timeStart={unix_time}&timeEnd={unix_time}`
    - Get articles in a site updated during a time interval: `GET /sites/{site_id}/updated_articles?timeStart={unix_time}&timeEnd={unix_time}`
1. playground
    - Get a title: `GET /playground/random`
    - Add a record: `POST /playground/add_record`