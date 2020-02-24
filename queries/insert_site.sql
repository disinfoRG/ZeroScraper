-- :name insert_site :insert
INSERT INTO Site
  (airtable_id, is_active, name, type, url, config, site_info)
VALUES
  (:airtable_id, :is_active, :name, :type, :url, :config, :site_info)
