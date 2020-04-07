import json
import requests
import os
import re
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
    archive_domain = "https://pttread.com/"
    board = re.search(r'bbs/(\w+)/', ptt["url"]).group(1).lower()
    identifier = re.search(r'M(.*)', ptt["url"]).group(0).strip(".html").replace('.', '-').lower()
    archive_url = archive_domain+board+'/'+identifier
    r = requests.get(archive_url)
    if r.status_code == 200:
        now = int(time.time())
        x = queries.insert_snapshot(article_id=ptt["article_id"],
                                    snapshot_at=now,
                                    raw_data=r.text)
        y = queries.update_article_snapshot_time(article_id=ptt["article_id"],
                                                 snapshot_count=ptt["snapshot_count"],
                                                 next_snapshot_at=0,
                                                 last_snapshot_at=now)
        time.sleep(uniform(3, 5))
        lost_ptt.remove(ptt)
    else:
        failed_ptt.append(ptt)

if failed_ptt:
    json.dump(failed_ptt, open("pttweb_failed.json", "w"))
