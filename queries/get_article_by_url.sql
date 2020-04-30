-- :name get_article_by_url :many
SELECT *
FROM Article
WHERE (url = :url and url_hash = :url_hash)
OR redirect_to = :url
