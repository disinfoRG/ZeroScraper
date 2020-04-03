-- :name get_site_stats :many
SELECT *
FROM SiteStats
WHERE
  site_id = :site_id
