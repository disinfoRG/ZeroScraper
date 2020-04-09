-- :name count_articles_discovered_in_interval :many
SELECT
	site_id, count(*) as discover_count
FROM
(
SELECT
	ArticleSnapshot.article_id, Article.site_id, Article.first_snapshot_at, ArticleSnapshot.snapshot_at
FROM
	ArticleSnapshot
INNER JOIN
	Article
ON
	ArticleSnapshot.article_id = Article.article_id
WHERE
	DATE(ArticleSnapshot.snapshot_at_date) = :date
) as A
WHERE A.first_snapshot_at = A.snapshot_at
GROUP BY A.site_id;
