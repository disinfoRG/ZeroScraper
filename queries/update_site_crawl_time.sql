-- :name update_site_crawl_time :affected
UPDATE Site
SET last_crawl_at = :last_crawl_at
WHERE site_id = :site_id
