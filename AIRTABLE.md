# Set up Airtable

0. create a base with an arbitrary name
1. create an empty table inside the base called `Sites`
2. Inside `Sites`, create the following fields

| Field name | Field type  | Type details  | Explanation | 
|:----------:|:-----------:|:-------------:|:-----------------------:|
|  id |  formula | formula=RECORD_ID()  | unique record id|
|  approved | checkbox  |   | if checked, the record would be sent to db |
|  is_active | checkbox  |  | if checked, the website would be crawled when doing `ns.py discover`|
|  name | Single line text  |   | name of the website|
|  url | URL  |   |  url of the website|
|  type | Single select  | 官媒、新聞網站、內容農場、組織官網、討論區看板 | type of the website|
|  article | Single line text | | website article url regex|
|  following | Single line text | | website subpages url regex|
|  depth | Number | format = Integer(2)| scrapy crawler settings DEPTH|
|  delay | Number | format = Decimal(1.0), Precision=1.000 |scrapy crawler settings DELAY |
|  ua | Single line text | |user agent string|
|  selenium | checkbox | |use selenium to load website or not  |
