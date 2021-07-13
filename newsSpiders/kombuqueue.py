import os
import kombu

queue_url = f"sqla+{os.getenv('DB_URL')}"


def connection():
    return kombu.Connection(
        queue_url,
        transport_options={
            "queue_tablename": "kombu_queue",
            "message_tablename": "kombu_message",
        },
    )

def snapshotsQueue(conn):
    return conn.SimpleQueue("newsSpiders.snapshots")
