-- :name delete_snapshot :affected
DELETE
FROM ArticleSnapshot
WHERE article_id = :article_id

