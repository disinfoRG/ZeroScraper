-- :name insert_snapshot :insert
INSERT INTO ArticleSnapshot
  (article_id, snapshot_at, raw_data)
VALUES
  (:article_id, :snapshot_at, :raw_data)
