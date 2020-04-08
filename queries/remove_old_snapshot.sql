-- :name delete_snapshot :affected
DELETE
FROM ArticleSnapshot
WHERE article_id = :article_id
AND snapshot_at != :last_snapshot_at

