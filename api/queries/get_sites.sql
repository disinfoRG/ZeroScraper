-- :name get_sites :many
SELECT
  site_id,
  name,
  url,
  type,
  is_active
FROM Site
