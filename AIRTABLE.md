# Set up Airtable

0. Create a base with an arbitrary name
1. Inside the base, create a table called `Sites`.
2. Inside `Sites`, create the following fields

| Field name | Field type  | Type details  | Explanation | 
|:----------:|:-----------:|:-------------:|:-----------------------:|
|  id |  formula | formula=RECORD_ID()  | unique record id|
|  approved | checkbox  |   | if checked, the record would be sent to db |
|  is_active | checkbox  |  | if checked, the website would be crawled when doing `ns.py discover`|
|  name | Single line text  |   | name of the website|
|  url | URL  |   |  url of the website|
|  type | Single select  |  | type of the website|
|  article | Single line text | | website article url regex|
|  following | Single line text | | url regex of pages in the website to find more articles in.|
|  depth | Number | format = Integer(2)| scrapy crawler settings DEPTH|
|  delay | Number | format = Decimal(1.0), Precision=1.000 |scrapy crawler settings DELAY |
|  ua | Single line text | |user agent string|
|  selenium | checkbox | |use selenium to load website or not  |
|  login_url | Single line text | | url of the login page for sites that required login.|


- if having more than 1 regex for `article` and `following`, use `; ` (semicolon+space) to connect the regex(es). e.g. `/news/cate/; /news/breaknews/; /vote2020/index`.
- `following`, `depth`, `delay`, `ua`, and `selenium` have [default settings](newsSpiders/types.py), can leave blank if want to use default. 