-- :name get_recent_articles :many
SELECT *
FROM Article
ORDER BY first_snapshot_at DESC
LIMIT :limit
