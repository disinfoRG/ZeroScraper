-- :name get_site_article_count :one
SELECT
  count(article_id) as article_count
FROM Article
WHERE
  site_id = :site_id
