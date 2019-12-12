from bs4 import BeautifulSoup
from readability import Document
from datetime import datetime
import sqlalchemy as db
import logging
import traceback
from helpers import connect_to_db
import jsonlines


class CleanHTML:
    def __init__(self, snapshot_infos):
        self.snapshot_infos = snapshot_infos

        # todo: remove later
        self.writer = jsonlines.open("../parser_output.jsonl", mode="w")

    @staticmethod
    def clean(one_snapshot_info):
        # meta tag
        soup = BeautifulSoup(one_snapshot_info["raw_data"], "html.parser")
        # meta property
        meta_property = {
            x["property"]: x["content"]
            for x in soup.find_all(
                lambda tag: tag.name == "meta"
                and "property" in tag.attrs.keys()
                and "content" in tag.attrs.keys()
            )
        }
        meta_name = {
            x["name"]: x["content"]
            for x in soup.find_all(
                lambda tag: tag.name == "meta"
                and "name" in tag.attrs.keys()
                and "content" in tag.attrs.keys()
            )
        }

        # content
        doc = Document(one_snapshot_info["raw_data"])
        # title
        title = doc.title()

        # main body
        s = doc.summary()
        soup = BeautifulSoup(s, "html.parser")

        # article text
        text = " ".join([" ".join(x.text.split()) for x in soup.find_all("p")])

        # links
        external_links = [x["href"] for x in soup.find_all("a", href=lambda x: x)]
        image_links = [
            x.get("data-src", x.get("src", x.get("data-original", "")))
            for x in soup.find_all("img")
        ]

        return {
            "meta_property": meta_property,
            "meta_name": meta_name,
            "title": title,
            "main_text": text,
            "external_links": external_links,
            "image_links": image_links,
        }

    def save(self, x):
        # to elastic search
        # r = requests.post(f"{es_url}/{index}", data=json.dumps(x))

        # to db
        # _, connection, tables = connect_to_db(env_keyword = "PARSED_DB_URL")
        # table_name = 'Content'
        # connection.execute(db.insert(tables[table_name], x))

        self.writer.write(x)

    def run(self):
        current_time_str = datetime.now().strftime("%Y-%m-%dT%H:%M%S")
        logging.basicConfig(
            filename=f"../.log/parser_{current_time_str}.log",
            format="%(asctime)s - %(message)s",
            level=logging.WARNING,
        )
        success = 0
        failure = 0
        logging.warning("Begin Parsing")

        for one_snapshot_info in self.snapshot_infos:
            try:
                parsed_content = self.clean(one_snapshot_info)
            except:
                logging.error(
                    f"article_id = {str(one_snapshot_info['article_id'])}, snapshot_at = {str(one_snapshot_info['snapshot_at'])} "
                    f"parsing failed \n{traceback.format_exc()}"
                )
                failure += 1
            else:
                content_to_save = {
                    "article_id": one_snapshot_info["article_id"],
                    "snapshot_at": one_snapshot_info["snapshot_at"],
                    **parsed_content,
                }
                self.save(content_to_save)
                success += 1
        logging.warning(
            f"Finish Parsing. \n Total: {len(self.snapshot_infos)} \n Succeeded: {success} \n Failed: {failure}"
        )


if __name__ == "__main__":
    _, conn, tables = connect_to_db()
    article_snapshot = tables["ArticleSnapshot"]
    q = article_snapshot.select()
    snapshot_infos = [dict(row) for row in conn.execute(q).fetchall()]
    clean = CleanHTML(snapshot_infos)
    clean.run()
