import json
import requests
import os
import time
from random import uniform
import pugsql
from tqdm import tqdm

queries = pugsql.module("./queries")
queries.connect(os.getenv("DB_URL"))
lost_ptt = json.load(open("lost_ptt.json"))
failed_ptt = list()
for i in tqdm(range(len(lost_ptt))):
    ptt = lost_ptt[i]
    archive_url = ptt["url"].replace("ptt", "pttweb")
    r = requests.get(archive_url, headers={"User-Agent": "Mozilla 5.0"})
    if r.status_code == 200:
        now = int(time.time())
        queries.insert_snapshot(article_id=ptt["article_id"],
                                snapshot_at=now,
                                raw_data=r.text)
        queries.update_article_snapshot_time(article_id=ptt["article_id"],
                                             snapshot_count=ptt["snapshot_count"],
                                             next_snapshot_at=0,
                                             last_snapshot_at=now)
        time.sleep(uniform(3, 5))
        lost_ptt.remove(ptt)
    else:
        print("Failed ", ptt)
        failed_ptt.append(ptt)

json.dump(failed_ptt, open("pttweb_failed.json", "w"))
