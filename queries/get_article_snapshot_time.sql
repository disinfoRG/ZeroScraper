-- :name get_article_snapshot_time :many
SELECT snapshot_at
FROM ArticleSnapshot
WHERE
  article_id = :article_id
