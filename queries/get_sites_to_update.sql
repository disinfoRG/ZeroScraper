-- :name get_sites_to_update :many
SELECT DISTINCT(site_id)
FROM Article
WHERE
  next_snapshot_at != 0
  AND next_snapshot_at < :current_time
  AND article_type IN ("Article", "PTT")

