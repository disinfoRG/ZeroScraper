-- :name get_site_by_url :one
SELECT *
FROM Site
WHERE
  url = :url
