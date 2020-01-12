from dotenv import load_dotenv

load_dotenv()

import multiprocessing
import os
import time
import logging
from datetime import datetime
import newsSpiders.crawler.discover
import pugsql

queries = pugsql.module("queries/")
queries.connect(os.getenv("DB_URL"))


def log_filename():
    filename = os.getenv("LOG_FILE", None)
    variables = {"current_time": datetime.now().strftime("%Y-%m-%dT%H:%M%S")}
    if filename is not None:
        for k, v in variables.items():
            filename = filename.replace("{" + k + "}", v)
    return filename


logging.basicConfig(
    filename=log_filename(),
    format="%(asctime)s - %(message)s",
    level=os.getenv("LOG_LEVEL", "DEBUG"),
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
