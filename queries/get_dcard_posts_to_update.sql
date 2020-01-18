-- :name get_post_latest_snapshot :one
select article_id, url, snapshot_count from Article
where article_type = 'Dcard' AND next_snapshot_at <> 0 AND  next_snapshot_at < :current_time