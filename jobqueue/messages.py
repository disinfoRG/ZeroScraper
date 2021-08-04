from pathlib import Path
import json
import python_jsonschema_objects as pjs

with (Path(__file__).parent / "schema/NewSnapshotMessage.json").open("r") as fp:
    builder = pjs.ObjectBuilder(json.load(fp))

ns = builder.build_classes()

NewSnapshotMessage = ns.NewSnapshotMessage
