-- :name get_one_dcard_site_posts_to_update :many
select article_id, url, snapshot_count from Article
where article_type = 'Dcard' AND site_id = :site_id AND next_snapshot_at <> 0 AND next_snapshot_at < :current_time