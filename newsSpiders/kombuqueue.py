import os
import json
from kombu import Connection
from kombu.pools import connections
import python_jsonschema_objects as pjs

queue_url = f"sqla+{os.getenv('DB_URL')}"

NEW_SNAPSHOT_SCHEMA = """
{"$schema":"http://json-schema.org/draft-04/schema#","$id":"http://0archive.tw/schemas/platform-schema.json","title":"New Snapshot Message","type":"object","properties":{"article_id":{"type":"integer"},"snapshot_at":{"type":"integer"},"events":{"type":"array","items":{"type":"object","properties":{"event_type":{"type":"string","enum":["scrape"]},"happened_at":{"type":"integer"},"succeeded":{"type":"boolean"},"result":{"type":"string"}},"required":["event_type","happened_at","succeeded","result"]}}},"required":["article_id","snapshot_at","events"]}
"""


builder = pjs.ObjectBuilder(json.loads(NEW_SNAPSHOT_SCHEMA))
ns = builder.build_classes()
NewSnapshotMessage = ns.NewSnapshotMessage


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
    with snapshotsQueue(conn) as queue:
        message = queue.get(block=True, timeout=4)
        print(message.payload)
        if ack:
            message.ack()
