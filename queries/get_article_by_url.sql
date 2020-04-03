-- :name get_article_by_url :many
SELECT *
FROM Article
WHERE url = :url
OR redirect_to = :url
