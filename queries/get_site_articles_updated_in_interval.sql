-- :name get_site_articles_updated_in_interval :many
SELECT *
FROM Article
WHERE
  site_id = :site_id
AND
  last_snapshot_at BETWEEN :time_start AND :time_end
AND
  last_snapshot_at <> first_snapshot_at;