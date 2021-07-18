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


def queue_snapshot(conn, article_id, snapshot_at):
    with snapshotsQueue(conn) as queue:
        message = NewSnapshotMessage(
            article_id=article_id,
            snapshot_at=snapshot_at,
            events=[
                ProcessEvent(
                    event_type="scrape",
                    happened_at=snapshot_at,
                    succeeded=True,
                    result="",
                )
            ],
        )
        queue.put(asdict(message))


def get_snapshot(conn, ack=True):
    with snapshotsQueue(conn) as queue:
        message = queue.get(block=True, timeout=4)
        print(message.payload)
        if ack:
            message.ack()
