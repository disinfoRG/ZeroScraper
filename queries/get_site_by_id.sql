-- :name get_site_by_id :one
SELECT *
FROM Site
WHERE
  site_id = :site_id
