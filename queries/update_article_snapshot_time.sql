-- :name update_article_snapshot_time :affected
UPDATE Article
SET
  last_snapshot_at = :last_snapshot_at,
  snapshot_count = :snapshot_count,
  next_snapshot_at = :next_snapshot_at
WHERE
  article_id = :article_id
