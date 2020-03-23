-- :name get_active_sites :many
SELECT *
FROM Site
WHERE
  is_active=1;
