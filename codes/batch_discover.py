import multiprocessing
import sqlalchemy as db
import os
import time
from helpers import connect_to_db


def discover(site_id):
    os.system(f"python execute_spiders.py -d --site_id {site_id}")


# get a bunch of site ids
engine, connection = connect_to_db()
site_table = db.Table("Site", db.MetaData(), autoload=True, autoload_with=engine)
query = db.select([site_table.c.site_id]).where(site_table.c.is_active)
site_ids = [x[0] for x in connection.execute(query).fetchall()]
connection.close()

# run
start_time = time.time()
pool = multiprocessing.Pool()
pool.map(discover, site_ids)
print(f"\nTime to complete = {time.time() - start_time:.2f} seconds\n")
