-- :name get_site_latest_article :one
SELECT *
FROM Article
WHERE
  article_id = (SELECT MAX(article_id) FROM Article where site_id = :site_id GROUP BY site_id);
