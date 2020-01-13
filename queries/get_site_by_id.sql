-- :name get_site_by_id :one
SELECT site_id, name, url, type, config
FROM Site
WHERE site_id = :site_id
