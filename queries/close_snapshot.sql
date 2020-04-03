-- :name close_snapshot :affected
UPDATE Article
set
    next_snapshot_at = 0
where
    article_id = :article_id