-- :name get_articles_to_update :many
SELECT *
FROM Article
WHERE
  site_id = :site_id
  AND next_snapshot_at != 0
  AND next_snapshot_at < :current_time
  AND article_type IN ("Article", "PTT")
ORDER BY next_snapshot_at ASC
-- set a hard limit on this: 2000 articles per site seems a good chunk of work
LIMIT 2000
