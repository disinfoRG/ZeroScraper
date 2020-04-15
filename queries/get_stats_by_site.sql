-- :name get_stats_by_site :many
SELECT site_id, DATE_FORMAT(date, "%Y-%m-%d") as date, new_article_count, updated_article_count
FROM SiteStats
WHERE
  site_id = :site_id
-- 30 days of stats should be quite enough for monitoring purposes
AND date >= DATE_SUB((select max(date) from SiteStats) , INTERVAL 30 DAY);
