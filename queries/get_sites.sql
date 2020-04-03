-- :name get_sites :many
SELECT
  site_id, type, name, url, airtable_id, is_active, last_crawl_at
FROM Site
