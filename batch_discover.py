import multiprocessing
import os
import time
import logging
from datetime import datetime
import newsSpiders.runner.discover
import pugsql

queries = pugsql.module("queries/")
queries.connect(os.getenv("DB_URL"))

current_time_str = datetime.now().strftime("%Y-%m-%dT%H:%M%S")
logging.basicConfig(
    filename=f".log/{current_time_str}.log",
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
site_infos = list(queries.get_sites_to_crawl())
sorted_site_infos = sorted(
    site_infos, key=lambda k: 0 if k["last_crawl_at"] is None else k["last_crawl_at"]
)

# run
start_time = time.time()
pool = multiprocessing.Pool()
pool.map(discover, sorted_site_infos)
# closing pool gracefully
pool.close()
pool.join()

logging.info(f"\nTime to complete = {time.time() - start_time:.2f} seconds\n")
