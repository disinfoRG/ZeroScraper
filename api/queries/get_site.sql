-- :name get_site :one
SELECT
  site_id,
  name,
  url,
  type
  airtable_id,
  is_active
FROM Site
WHERE site_id = :id
