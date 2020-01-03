import multiprocessing
import sqlalchemy as db
import time
import logging
from datetime import datetime
from helpers import connect_to_db
import newsSpiders.runner.discover


current_time_str = datetime.now().strftime("%Y-%m-%dT%H:%M%S")
logging.basicConfig(
    filename=f"../.log/{current_time_str}.log",
    format="%(asctime)s - %(message)s",
    level=logging.INFO,
)


def discover(site_info):
    site_start_time = time.time()
    site_id = site_info["site_id"]
    site_name = site_info["name"]
    logging.info(f"Begin discover new articles on site {site_id} {site_name}")
    newsSpiders.runner.discover.run(site_id)
    logging.info(
        f"Finish site {site_id} {site_name}. Process time = {time.time()-site_start_time:.2f} seconds"
    )


# get a bunch of site ids
engine, connection, tables = connect_to_db()
site_table = tables["Site"]
query = db.select(
    [site_table.c.site_id, site_table.c.name, site_table.c.last_crawl_at]
).where(site_table.c.is_active)
site_infos = [dict(x) for x in connection.execute(query).fetchall()]
sorted_site_infos = sorted(
    site_infos, key=lambda k: 0 if k["last_crawl_at"] is None else k["last_crawl_at"]
)
connection.close()

# run
start_time = time.time()
pool = multiprocessing.Pool()
pool.map(discover, sorted_site_infos)
logging.info(f"\nTime to complete = {time.time() - start_time:.2f} seconds\n")
