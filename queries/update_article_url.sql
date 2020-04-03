-- :name update_article_url :affected
UPDATE Article
SET
  url = :url,
  url_hash = :url_hash
WHERE
  article_id = :article_id
