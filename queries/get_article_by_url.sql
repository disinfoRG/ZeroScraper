-- :name get_article_by_url :one
SELECT
  article_id
FROM Article
WHERE
  url_hash = :url_hash AND url = :url
