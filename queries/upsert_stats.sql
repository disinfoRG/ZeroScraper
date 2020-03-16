-- :name upsert_stats :insert
INSERT INTO SiteStats
  (site_id, date, new_article_count, updated_article_count)
VALUES
  (:site_id, :date, :discover_count, :update_count)
ON DUPLICATE KEY UPDATE
  new_article_count = :discover_count, updated_article_count = :update_count;
