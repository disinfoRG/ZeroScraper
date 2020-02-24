-- :name update_site :affected
UPDATE Site
SET
  is_active = :is_active, name = :name, type = :type, url = :url, config = :config
WHERE
  site_id = :site_id
