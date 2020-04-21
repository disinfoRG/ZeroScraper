-- :name get_stats_by_date :many
SELECT site_id, DATE_FORMAT(date, "%Y-%m-%d") as date, new_article_count, updated_article_count
FROM SiteStats
WHERE
  date = :date
