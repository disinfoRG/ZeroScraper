-- :name count_site_article_discovered_in_interval :one
SELECT count(*) as article_count
FROM Article
WHERE
  site_id = :site_id
AND
  first_snapshot_at >= :discover_from
AND
  first_snapshot_at <= :discover_until
