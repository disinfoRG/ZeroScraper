import json

airtable_csv = open(
    "../data/airtable_sites.csv", encoding="utf8"
)  # csv downloaded from airtable
local_csv = open("../data/url_map.csv", encoding="utf8")
sites = {}

site_types = {
    "官媒": "official_media",
    "新聞網站": "news_website",
    "內容農場": "content_farm",
    "組織官網": "organization_website",
    "Fb 專頁": "fb_page",
    "Fb 公開社團": "fb_public_group",
    "Ptt 看板": "ptt_board",
    "YouTube 頻道": "youtube_channel",
    "YouTube 帳號": "youtube_user",
}

header = airtable_csv.readline()  # discard header
for line in airtable_csv:
    id, name, url, type, *rest = line.split(",")
    sites[id] = {"type": site_types.get(type, "?"), "name": name, "url": url}

header = local_csv.readline()  # discard header
for line in local_csv:
    id, name, url, type, article, following = line.split(",")
    article = article.strip()
    following = following.strip()
    if id in sites:
        config = {}
        if article != "":
            config["article"] = article
        if following != "":
            config["following"] = following
        if config:
            sites[id]["config"] = config

open("../migrations/init_sites.sql", "w").close()  # clear sql file content
sql = open("../migrations/init_sites.sql", "a")

sql.write("TRUNCATE TABLE `Site`;\n")
for original_id, site in sites.items():
    if "config" in site:
        sql.write(
            "INSERT INTO `Site`(type, name, url, config) VALUES('{0}', '{1}', '{2}', '{3}');\n".format(
                site["type"], site["name"], site["url"], json.dumps(site["config"])
            )
        )
    else:
        sql.write(
            "INSERT INTO `Site`(type, name, url) VALUES('{0}', '{1}', '{2}');\n".format(
                site["type"], site["name"], site["url"]
            )
        )

airtable_csv.close()
local_csv.close()
sql.close()
