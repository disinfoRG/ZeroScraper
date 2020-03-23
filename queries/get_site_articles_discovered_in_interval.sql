-- :name get_site_articles_discovered_in_interval :many
SELECT *
FROM Article
WHERE
  site_id = :site_id
AND
  first_snapshot_at BETWEEN :time_start AND :time_end;