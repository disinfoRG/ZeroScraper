-- :name get_stats_by_site :many
SELECT *
FROM SiteStats
WHERE
  site_id = :site_id
-- 30 days of stats seems quite enough for monitoring purposes
AND DATE(date) >= DATE_SUB((select max(DATE(date)) from SiteStats) , INTERVAL 30 DAY);
