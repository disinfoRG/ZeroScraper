import os
from kombu import Connection
from kombu.pools import connections

queue_url = f"sqla+{os.getenv('DB_URL')}"


def connection(block=True):
    conn = Connection(
        queue_url,
        transport_options={
            "queue_tablename": "kombu_queue",
            "message_tablename": "kombu_message",
        },
    )
    return connections[conn].acquire(block)

def snapshotsQueue(conn):
    return conn.SimpleQueue("newsSpiders.snapshots")
