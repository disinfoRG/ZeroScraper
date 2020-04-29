ZeroScraper API
===
## Contents
1. [API endpoints](#api-endpoints)
    1. [authentication](#authentication)
    2. [system monitoring](#api-monitor)
    3. [stats](#stats)
    4. [articles](#articles)
    5. [sites](#sites)
    6. [publications](#publications)
    7. [playground](#playground)
    
2. [Using Browser](#using-browser)
3. [Using Command-line tools](#using-command-line-tools)
---
### API endpoints
1. #####authentication
    - `POST /login?username=:username&password=:password`: To login. 

        ```json
        {
          "message": "Login successfully.",
          "access_token": "xxx"
        }  
        ```
    - `POST /logout`: To logout.

1. #####system monitoring

    - `GET /health`: Check if scheduled scraping activity is executing as expected: 
    
        If the latest inserted article is less than 15 minutes ago, return `okay`. Otherwise, 
`not okay`. 

    - `GET /variables`: Get all variables 
        ```json
        {
          "message": "returning all variables", 
          "result": [
            {
              "key": "discover:pid", 
              "value": "4396"
            }, 
            {variable info},
            ...
          ]
        }
        ```
    - `GET /variables?key=:key`: Get variables by key
        ```json
        {
          "message": "returning variables with key :key", 
          "result": [
              {variable info}
          ]
        }
        ```
1. #####stats
    - `GET /stats`: Get stats of all days and sites 
        
        ```json
        {
          "message": "Returning all stats", 
          "result": [
            {
              "date": "2020-03-01", 
              "site_id": 1, 
              "new_article_count": 134, 
              "updated_article_count": 0
            },
            {stats},
            {stats}.
            ...
          ]
        }
        ```
     
    - `GET /stats?date=:date`: Get stats of all sites on a day, e.g. `GET /stats?date=2020-04-05`
        ```json
        {
          "message": "Return stats of all sites on :date",
          "result": [
            {stats},
            {stats}, 
            ...
          ]
        }
        ```
    - `GET /stats?site_id=:id`: Get stats of a site, but only return stats of the last 30 days.
        
        ```json
        {
          "message": "Returning stats of site :id from the last 30 days.", 
          "result": [
            {stats},
            {stats},
            ...
          ]
        }
        ```

1. #####articles

    - `GET /articles`: Returning 10 recent articles.
        
        ```json
        {
          "message": "Returning 10 most recent articles.", 
          "result": [
            {
              "article_id": 3939173, 
              "article_type": "Article", 
              "first_snapshot_at": 1588107403, 
              "last_snapshot_at": 1588107403, 
              "next_snapshot_at": 1588193803, 
              "redirect_to": null, 
              "site_id": 105, 
              "snapshot_count": 1, 
              "url": xxx, 
              "url_hash": "43445058"
            }, 
            {article info},
            {article info},
            ...
          ]
        }
        ```
    - `GET /articles?url=:url`. Get articles with url, only for exact match. 
    The query find matches in both requested url and redirected url. 
        
        ```json
        {
          "message": "Returning articles that matches url :url,
          "result": [
             {article info},
             {article info},
             ...
          ]
        }
        ```
    - `GET /articles/:id`: Get article info with article_id: 

        ```json
        {
          "message": "Returning article with id :id", 
          "result": {article info}
        }
        ```

1. #####sites

    - `GET /sites`: Get all sites. 

        ```json
        {
          "message": "Returning all sites",
          "result": [
            {
              "airtable_id": "xxx",
              "config": "{...}",
              "is_active": 1,
              "last_crawl_at": 1588123660,
              "name": "yyy",
              "site_id": 100,
              "site_info": "{...}",
              "type": "zzz",
              "url": "ooo"
            },
            {site info},
            {site info},
            ...
          ]
        }
        ```
    - `GET /sites/active`: Get all active sites. 

        ```json
        {
          "message": "Returning active sites",
          "result": [
            {site info},
            {site info},
            ...
          ]
        }
        ```
    - `GET /sites/:id/article_count`: Get article count in a site. 

        ```json
        {
          "message": "Returning article count of site :id",
          "result": {
            "site": {site :id info}
            "article_count": 100
          }
        }
        ```
    - `GET /sites/:id/latest_article`: Get most recently added article of a site: 

        ```json
        {
          "message": "Returning latest article from site :id",
          "result": {
            "latest_article": {article info},
            "site": {site :id info}
        }
        ```

1. #####publications

    - `GET /publications?q=:search_string`: Get publications where title or text contains the search string.

        ```json
        {
          "message": "Return publications that matches :search_string",
          "result": [
            {publication info},
            {publication info},
            ...
          ]
        }
        ```

1. #####playground

    - `GET /playground/random`: Get a random publication title. 

        ```json
        {
          "publication_id": "xxx",
          "text": "yyy"
        }
        ```
    - `POST /playground/add_record`: Add a record. 
        ```json
      {
          "message": "Add new record successfully.",
          "record_id": 123,
      }
        ```

### Using Browser
1. login first: `GET /login` to fill out the form and submit.


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

