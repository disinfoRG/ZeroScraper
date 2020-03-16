-- :name count_articles_discovered_in_interval :many
SELECT site_id, count(*) as discover_count
FROM Article
WHERE
  first_snapshot_at >= :time_start
AND
  first_snapshot_at <= :time_end
GROUP BY site_id;