-- :name update_article_snapshot_time :affected
update Article
set
last_snapshot_at = :crawl_time,
snapshot_count = :snapshot_count,
next_snapshot_at = :next_snapshot_at

where article_id = :article_id