import os
from kombu import Connection
from kombu.pools import connections
from .messages import NewSnapshotMessage

queue_url = f"sqla+{os.getenv('DB_URL')}"


def connection(url=queue_url, block=True):
    conn = Connection(
        url,
        transport_options={
            "queue_tablename": "kombu_queue",
            "message_tablename": "kombu_message",
        },
    )
    return connections[conn].acquire(block)


def snapshots_queue(conn):
    return conn.SimpleQueue("newsSpiders.snapshots")


def queue_snapshot(conn, article_id, snapshot_at):
    with snapshots_queue(conn) as queue:
        message = NewSnapshotMessage(
            article_id=article_id,
            snapshot_at=snapshot_at,
            events=[
                {
                    "event_type": "scrape",
                    "happened_at": snapshot_at,
                    "succeeded": True,
                    "result": "",
                }
            ],
        )
        queue.put(message.serialize(sort_keys=True))


def get_snapshot(conn, ack=True):
    with snapshots_queue(conn) as queue:
        message = queue.get(block=True, timeout=4)
        if ack:
            message.ack()
