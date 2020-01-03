-- :name upsert_site :insert
INSERT INTO Site
(airtable_id, is_active, name, type, url, config, site_info)
VALUES
(:airtable_id, :is_active, :name, :type, :url, :config, :site_info)
ON DUPLICATE KEY UPDATE
is_active = :is_active, name = :name, type = :type, url = :url, config = :config
