-- :name insert_snapshot :insert
INSERT INTO ArticleSnapshot
  (article_id, snapshot_at, raw_data, snapshot_at_date)
VALUES
  (:article_id, :snapshot_at, :raw_data, FROM_UNIXTIME(:snapshot_at))
