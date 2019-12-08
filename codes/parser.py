from bs4 import BeautifulSoup
import sqlalchemy as db
import pickle
import htmldate
from helpers import connect_to_db

# todo:
#   extract meta?
#   write a wrapper


class CleanHTML:
    def __init__(self, article_id, raw_data, site_id=None):
        self.article_id = article_id
        self.raw_data = raw_data

        engine, conn, tables = connect_to_db()
        # site = db.Table("Site", db.MetaData(), autoload=True, autoload_with=engine)
        article = tables["Article"]
        if not site_id:
            query = db.select([article.c.site_id]).where(
                article.c.article_id == int(article_id)
            )
            site_id = conn.execute(query).fetchone()[0]
        # get css
        css_config = pickle.load(open("../css.pickle", "rb"))
        self.main_body_css = css_config[site_id]["body_css"]

    def clean(self):
        soup = BeautifulSoup(self.raw_data, "html.parser")
        # title
        title = soup.find("title").text.strip()
        # date - not 100% accurate
        guess_date = htmldate.find_date(self.raw_data)

        # main body
        main_body = soup.select_one(self.main_body_css)

        # article text
        text = " ".join([" ".join(x.text.split()) for x in main_body.find_all("p")])

        # links
        external_links = [x["href"] for x in main_body.find_all("a", href=lambda x: x)]
        image_links = [
            x["src"] if "src" in x.attrs.keys() else x["data-src"]
            for x in main_body.find_all("img")
            if "src" in x.attrs.keys() or "data-src" in x.attrs.keys()
        ]

        return {
            "title": title,
            "first_published_date": guess_date,
            "content": text,
            "external_links": external_links,
            "image_links": image_links,
        }

    def save(self):
        pass


if __name__ == "__main__":
    from datetime import datetime
    import logging

    current_time_str = datetime.now().strftime("%Y-%m-%dT%H:%M%S")
    logging.basicConfig(
        filename=f"../.log/parser_{current_time_str}.log",
        format="%(asctime)s - %(message)s",
        level=logging.INFO,
    )

    test_articles = (
        44669,
        6748,
        7353,
        4800,
        16700,
        37397,
        36199,
        647,
        44596,
        44662,
        55058,
        51588,
        44930,
        5032,
        42637,
        7247,
        130540,
        11178,
        45856,
        40175,
        133861,
        57166,
        48292,
        108021,
        131877,
        14019,
        84163,
        63908,
        23451,
        44215,
        49767,
        22848,
        24020,
        43760,
        108733,
        45644,
        25429,
        24589,
        63546,
        52517,
        65421,
        127031,
        35585,
        35582,
        35691,
        35623,
        35897,
        48802,
        47990,
        44508,
        40051,
    )
    engine, connection = connect_to_db()
    article_snapshot = db.Table(
        "ArticleSnapshot", db.MetaData(), autoload=True, autoload_with=engine
    )
    get_article_snapshot_query = f"Select * from ArticleSnapshot where article_id in {test_articles} GROUP BY article_id"
    article_meta = [
        dict(row) for row in connection.execute(get_article_snapshot_query).fetchall()
    ]
    print(len(article_meta))
    clean_articles = []
    for i in range(len(article_meta)):
        raw_html = article_meta[i]["raw_data"]
        article_id = article_meta[i]["article_id"]
        print(i, article_id)
        c = CleanHTML(article_id, raw_html)
        try:
            result = c.clean()
            result["article_id"] = article_id
            result["snapshot_at"] = article_meta[i]["snapshot_at"]
        except:
            logging.error(
                f"{str(article_id)}-{str(article_meta[i]['snapshot_at'])} parsing failed"
            )
        else:
            clean_articles.append(result)

    import pandas as pd

    df = pd.DataFrame(clean_articles)
    df.to_csv("../test_clean.csv", index=False)

    connection.close()
