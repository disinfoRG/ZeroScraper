-- :name get_recent_articles :many
SELECT *
FROM Article
ORDER BY article_id DESC
LIMIT :limit
