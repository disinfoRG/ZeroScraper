-- :name get_site_articles :one
SELECT
  count(*) AS count
FROM Article
WHERE site_id = :site_id

