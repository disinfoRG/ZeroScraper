-- :name get_sites_count :one
SELECT
  count(*) AS sites_count
FROM Site
