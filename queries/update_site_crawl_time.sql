-- :name update_site_crawl_time :affected
update Site set last_crawl_at = :crawl_time
where site_id = :site_id