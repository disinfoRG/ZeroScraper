-- :name upsert_site :insert
INSERT INTO Site
(airtable_id, name, type, url, config, site_info)
VALUES
(:airtable_id, :name, :type, :url, :config, :site_info)
ON DUPLICATE KEY UPDATE
name = :name, type = :type, url = :url, config = :config, site_info = :site_info
