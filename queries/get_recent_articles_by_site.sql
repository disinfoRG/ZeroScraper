-- :name get_recent_articles_by_site :many
SELECT *
FROM Article
WHERE
  site_id = :site_id
ORDER BY first_snapshot_at DESC
LIMIT :limit
