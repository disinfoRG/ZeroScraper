-- :name get_max_snapshot_at :one
SELECT max(snapshot_at) as max_snapshot_at
from ArticleSnapshot;