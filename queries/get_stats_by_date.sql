-- :name get_stats_by_date :many
SELECT *
FROM SiteStats
WHERE
  date = :date
