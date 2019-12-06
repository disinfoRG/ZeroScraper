-- :name get_sites_stats :many
SELECT
  Article.site_id AS id,
  Site.name AS name,
  Site.url AS url,
  count(*) AS articles_count
FROM Article
  JOIN Site ON Site.site_id = Article.site_id
GROUP BY Article.site_id

