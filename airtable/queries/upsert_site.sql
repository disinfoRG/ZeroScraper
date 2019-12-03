-- :name upsert_site :insert
INSERT INTO Site
(airtable_id, name, type, url, config)
VALUES
(:airtable_id, :name, :type, :url, :config)
ON DUPLICATE KEY UPDATE
name = :name, type = :type, url = :url, config = :config
