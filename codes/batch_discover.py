import multiprocessing
import sqlalchemy as db
import os
import time
import logging
from datetime import datetime
from helpers import connect_to_db
import sys

python_path = sys.executable

current_time_str = datetime.now().strftime("%Y-%m-%dT%H:%M%S")
logging.basicConfig(
    filename=f"../.log/discover_{current_time_str}.log",
    format="%(asctime)s - %(message)s",
    level=logging.INFO,
)


def discover(site_info):
    site_start_time = time.time()
    site_id = site_info["site_id"]
    site_name = site_info["name"]
    logging.info(f"Begin discover new articles on site {site_id} {site_name}")
    os.system(f"{python_path} execute_spiders.py -d --site_id {site_id}")
    logging.info(
        f"Finish site {site_id} {site_name}. Process time = {time.time()-site_start_time:.2f} seconds"
    )


# get a bunch of site ids
engine, connection, tables = connect_to_db()
site_table = tables["Site"]
query = db.select([site_table.c.site_id, site_table.c.name]).where(
    site_table.c.is_active
)
site_infos = [dict(x) for x in connection.execute(query).fetchall()]
connection.close()

# run
start_time = time.time()
pool = multiprocessing.Pool()
pool.map(discover, site_infos)
logging.info(f"\nTime to complete = {time.time() - start_time:.2f} seconds\n")
