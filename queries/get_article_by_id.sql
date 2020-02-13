-- :name get_article_by_id :one
SELECT *
FROM Article
WHERE
  article_id = :article_id
