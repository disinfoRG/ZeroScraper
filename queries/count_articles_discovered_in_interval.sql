-- :name count_articles_discovered_in_interval :many
SELECT
	site_id, count(*) as discover_count
FROM
(
SELECT
	Snapshot.article_id, Article.site_id, Article.first_snapshot_at, Snapshot.snapshot_at
FROM
	ArticleSnapshot202003 as Snapshot
INNER JOIN
	Article
ON
	Snapshot.article_id = Article.article_id
WHERE
	Snapshot.snapshot_at between :time_start and :time_end
) as A
WHERE A.first_snapshot_at = A.snapshot_at
GROUP BY A.site_id;