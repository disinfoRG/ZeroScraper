import os
from kombu import Connection
from kombu.pools import connections
from newsSpiders.types import NewSnapshotMessage, ProcessEvent, asdict

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


def snapshotsQueue(conn):
    return conn.SimpleQueue("newsSpiders.snapshots")


def queue_snapshot(conn, article, snapshot):
    with snapshotsQueue(conn) as queue:
        message = NewSnapshotMessage(
            article_id=article["article_id"],
            snapshot_at=snapshot["snapshot_at"],
            events=[
                ProcessEvent(
                    event_type="scrape",
                    happened_at=snapshot["snapshot_at"],
                    succeeded=True,
                    result="",
                )
            ],
        )
        queue.put(asdict(message))
