-- :name upsert_stats :insert
INSERT INTO SiteStats
  (site_id, date, new_posts_count, revisit_posts_count)
VALUES
  (:site_id, :date, :discover_count, :update_count)
ON DUPLICATE KEY UPDATE
  new_posts_count = :discover_count, revisit_posts_count = :update_count;
