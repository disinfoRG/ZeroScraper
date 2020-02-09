-- :name get_article_by_url :one
SELECT *
FROM Article
WHERE url = :url
