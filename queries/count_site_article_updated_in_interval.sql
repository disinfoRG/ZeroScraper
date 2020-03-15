-- :name count_articles_updated_in_interval :many
SELECT site_id, count(*) as update_count
FROM Article
WHERE
  last_snapshot_at >= :time_start
AND
  last_snapshot_at <= :time_end
AND
  last_snapshot_at <> first_snapshot_at
GROUP BY site_id;