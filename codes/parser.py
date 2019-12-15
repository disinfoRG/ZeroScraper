from bs4 import BeautifulSoup
from readability import Document
from datetime import datetime
import logging
from helpers import connect_to_db
import jsonlines

# todo:
#   extract meta?
#   logging problem


class CleanHTML:
    def __init__(self, snapshot_infos):
        self.snapshot_infos = snapshot_infos

        # todo: remove later
        self.writer = jsonlines.open("../parser_output.jsonl", mode="w")

    @staticmethod
    def clean(one_snapshot_info):
        doc = Document(one_snapshot_info["raw_data"])
        # title
        title = doc.title()

        # main body
        s = doc.summary()
        soup = BeautifulSoup(s, "html.parser")

        # date - not 100% accurate
        # guess_date = htmldate.find_date(self.raw_data)

        # article text
        text = " ".join([" ".join(x.text.split()) for x in soup.find_all("p")])

        # links
        external_links = [x["href"] for x in soup.find_all("a", href=lambda x: x)]
        image_links = [x["data-src"] for x in soup.find_all("img")]

        return {
            "title": title,
            "main_text": text,
            "external_links": external_links,
            "image_links": image_links,
        }

    def save(self, x):
        # to elastic search
        # r = requests.post(f"{es_url}/{index}", data=json.dumps(x))

        self.writer.write(x)

    def run(self):
        current_time_str = datetime.now().strftime("%Y-%m-%dT%H:%M%S")
        logging.basicConfig(
            filename=f"../.log/parser_{current_time_str}.log",
            format="%(asctime)s - %(message)s",
            level=logging.INFO,
        )
        for one_snapshot_info in self.snapshot_infos:
            try:
                parsed_content = self.clean(one_snapshot_info)
            except:
                logging.error(
                    f"{str(one_snapshot_info['article_id'])}-{str(one_snapshot_info['snapshot_at'])} "
                    f"parsing failed"
                )
            else:
                content_to_save = {
                    "article_id": one_snapshot_info["article_id"],
                    "snapshot_at": one_snapshot_info["snapshot_at"],
                    **parsed_content,
                }
                self.save(content_to_save)


if __name__ == "__main__":
    _, conn, tables = connect_to_db()
    article_snapshot = tables["ArticleSnapshot"]
    q = article_snapshot.select()
    snapshot_infos = [dict(row) for row in conn.execute(q).fetchall()[-20:]]
    clean = CleanHTML(snapshot_infos)
    clean.run()
